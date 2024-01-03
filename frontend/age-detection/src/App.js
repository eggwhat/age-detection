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

    const handleImageUpload = async (e) => {
        const file = e.target.files[0];
        if (file) {
            const formData = new FormData();
            for (const fileData of e.target.files) {
                formData.append('files', fileData);
            }

            const response = await fetch('http://127.0.0.1:8000/detect-age/multiple', {
                method: 'POST',
                body: formData,
            });

            if (response.ok) {
                const result = await response.json();
                const age = result.age;
                const imageBlob = await fetch(`data:image/jpeg;base64,${result.image}`).then(r => r.blob());
                const imageUrl = URL.createObjectURL(imageBlob);

                const link = document.createElement('a');
                link.href = imageUrl;
                link.download = `age_${age}.jpeg`;
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
            } else {
                console.error('Image upload failed');
            }
        }
    };

    const handleVideoUpload = async (e) => {
        const file = e.target.files[0];
        if (file) {
            const formData = new FormData();
            formData.append('file', file);

            const response = await fetch('http://127.0.0.1:8000/detect-age/video', {
                method: 'POST',
                body: formData,
            });

            if (response.ok) {
                const data = await response.blob();
                const videoURL = URL.createObjectURL(data);
                setProcessedVideoData(videoURL);
            } else {
                console.error('Video upload failed');
            }
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
                <input type="file" accept="image/*" onChange={handleImageUpload} hidden id="imageUpload"/>
                <label htmlFor="imageUpload" className="upload-button">Upload Image</label>

                <input type="file" accept="video/*" onChange={handleVideoUpload} hidden id="videoUpload"/>
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

