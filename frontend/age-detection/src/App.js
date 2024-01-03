import React, {useEffect, useRef, useState} from 'react';
import Webcam from 'react-webcam';
import Logo from './assets/logo.svg';
import './App.css';

function App() {
    const webcamRef = useRef(null);
    const [ws, setWs] = useState(null);
    const [processedFrame, setProcessedFrame] = useState(null);
    const [isPredictionReceived, setIsPredictionReceived] = useState(false);

    useEffect(() => {
        const websocket = new WebSocket('ws://127.0.0.1:8000/detect-age/ws');
        setWs(websocket);

        websocket.onopen = () => console.log('WebSocket Connected');
        websocket.onmessage = (event) => {
            setProcessedFrame(`data:image/jpeg;base64,${event.data}`);
            setIsPredictionReceived(true);
        };
        websocket.onclose = () => console.log('WebSocket Disconnected');
        websocket.onerror = error => console.log('WebSocket Error: ', error);

        return () => {
            websocket.close();
        };
    }, []);

    useEffect(() => {
        if (!isPredictionReceived) {
            const interval = setInterval(() => {
                captureAndSendFrame();
            }, 1000 / 10);

            return () => clearInterval(interval);
        }
    }, [ws]);

    const captureAndSendFrame = () => {
        if (webcamRef.current && ws?.readyState === WebSocket.OPEN) {
            const imageSrc = webcamRef.current.getScreenshot();

            if (imageSrc) {
                ws.send(imageSrc.split(',')[1]);
            }
        }
    };

    const [processedImageData, setProcessedImageData] = useState(null);
    const [processedVideoData, setProcessedVideoData] = useState(null);

   const [selectedFiles, setSelectedFiles] = useState([]);

    const handleFileSelect = (event) => {
        setSelectedFiles([...event.target.files]);
        handleImageUpload();
    };

    const handleImageUpload = async () => {
        if (selectedFiles.length === 0) {
            alert('Please select one or more files.');
            return;
        }

        const formData = new FormData();
        selectedFiles.forEach(file => {
            formData.append('files', file);
        });

        try {
            const response = await fetch('http://127.0.0.1:8000/detect-age/multiple', {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                throw new Error('Server responded with an error.');
            }

            const blob = await response.blob();
            const downloadUrl = window.URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.href = downloadUrl;
            link.download = 'images.zip';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            window.URL.revokeObjectURL(downloadUrl);

        } catch (error) {
            console.error('Error:', error);
            alert('Upload failed. Please try again.');
        }
    };

    const handleVideoFileSelect = (event) => {
        const videos = Array.from(event.target.files).filter(file =>
            file.type.startsWith('video/')
        );
        setSelectedFiles(videos);
        handleVideoUpload();
    };

    const handleVideoUpload = async () => {
        if (selectedFiles.length === 0) {
            alert('Please select one or more video files.');
            return;
        }

        const formData = new FormData();
        selectedFiles.forEach(file => {
            formData.append('files', file);
        });

        try {
            const response = await fetch('http://127.0.0.1:8000/detect-age/video', {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                throw new Error('Server responded with an error.');
            }

            const blob = await response.blob();
            const downloadUrl = window.URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.href = downloadUrl;
            link.download = 'videos.zip';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            window.URL.revokeObjectURL(downloadUrl);

        } catch (error) {
            console.error('Error:', error);
            alert('Upload failed. Please try again.');
        }
    };

    return (
        <div className="container">
            <header>
                <img src={Logo} alt="Age Detection App Logo" className="logo"/>
                <h1>Discover Your Age</h1>
                <p>Our advanced AI will guess your age from your webcam feed. Give it a try!</p>
            </header>
            <main>
                <div className="video-container">
                    {/*{!isPredictionReceived ? (*/}
                    <div className="webcam-feed">
                        <Webcam
                            audio={false}
                            ref={webcamRef}
                            screenshotFormat="image/jpeg"
                            videoConstraints={{width: 640, height: 480}}
                        />
                    </div>
                    {/*) : (*/}
                    <div className="result-display">
                        {processedFrame && <img src={processedFrame} alt="Processed Frame"/>}
                    </div>
                    {/*)}*/}
                </div>
                <input type="file" accept="image/*" onChange={handleFileSelect} hidden id="imageUpload"/>
                <label htmlFor="imageUpload" className="upload-button">Upload Image</label>

                <input type="file" accept="video/*" onChange={handleVideoFileSelect} hidden id="videoUpload"/>
                <label htmlFor="videoUpload" className="upload-button">Upload Video</label>
                {processedImageData && (
                    <img src={`data:image/jpeg;base64,${processedImageData}`} alt="Processed Image"/>
                )}
                {processedVideoData && (
                    <video controls src={processedVideoData}/>
                )}
            </main>
            <footer>
                <p>&copy; 2024 Age Detection App</p>
            </footer>
        </div>
    );
}

export default App;

