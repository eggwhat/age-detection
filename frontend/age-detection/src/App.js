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
            }, 1000 / 5);

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
        const files = [...event.target.files];
        setSelectedFiles(files);
        handleImageUpload(files);
    };

    const handleImageUpload = async (files) => {

        if (files.length === 0) {
            alert('Please select a directory with one or more files.');
            return;
        }

        if (files.length > 40) {
            alert('Please select a directory with fewer than 40 files.');
            return;
        }

        const formData = new FormData();
        files.forEach(file => {
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


    const [isLoading, setIsLoading] = useState(false);
    const [isWebcamActive, setIsWebcamActive] = useState(true);

    const handleVideoUpload = async (file) => {
        if (!file) {
            alert('Please select a video file.');
            return;
        }

        setIsLoading(true);
        setIsWebcamActive(false);

        const formData = new FormData();
        formData.append('file', file);

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
            link.download = 'processed_video.mp4';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            window.URL.revokeObjectURL(downloadUrl);

        } catch (error) {
            console.error('Error:', error);
            alert('Upload failed. Please try again.');
        } finally {
            setIsLoading(false);
            setIsWebcamActive(true); // Reactivate webcam when video upload ends
        }
    };

    const Loader = () => (
        <div className="spinner-container">
            <div className="spinner"></div>
        </div>
    );

    return (
        <div className="container">
            <header>
                <img src={Logo} alt="Age Detection App Logo" className="logo"/>
                <h1>Discover Your Age</h1>
                <p>Our advanced AI will guess your age from your webcam feed. Give it a try!</p>
            </header>
            <main>
                <div className="button-container">
                    <input
                        type="file"
                        accept="image/*"
                        onChange={handleFileSelect}
                        multiple
                        directory=""
                        webkitdirectory=""
                        hidden
                        id="imageUploadDirectory"
                    />
                    <label htmlFor="imageUploadDirectory" className="upload-button">Upload Image Directory</label>

                    <input
                        type="file"
                        accept="video/*"
                        onChange={(e) => handleVideoUpload(e.target.files[0])}
                        hidden
                        id="videoUpload"
                    />
                    <label htmlFor="videoUpload" className="upload-button">Upload Video</label>
                </div>

                {processedImageData && (
                    <img src={`data:image/jpeg;base64,${processedImageData}`} alt="Processed Image"/>
                )}
                {processedVideoData && (
                    <video controls src={processedVideoData}/>
                )}

                <div className="video-container">
                    {isWebcamActive && (
                        <div className="webcam-feed">
                            <Webcam
                                audio={false}
                                ref={webcamRef}
                                screenshotFormat="image/jpeg"
                                videoConstraints={{width: 640, height: 480}}
                            />
                        </div>
                    )}
                    {!isWebcamActive && isLoading && <Loader/>}
                    {isWebcamActive && (
                        <div className="result-display">
                            {processedFrame && <img src={processedFrame} alt="Processed Frame"/>}
                        </div>
                    )}
                    {!isWebcamActive && isLoading && <Loader/>}
                </div>
            </main>
            <footer>
                <p>&copy; 2024 Age Detection App</p>
            </footer>
        </div>
    );
}

export default App;

