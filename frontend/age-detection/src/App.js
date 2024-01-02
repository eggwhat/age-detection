import React, { useEffect, useRef, useState } from 'react';
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
            }, 1000);

            return () => clearInterval(interval);
        }
    }, [ws]);

    const captureAndSendFrame = () => {
        if (webcamRef.current && ws?.readyState === WebSocket.OPEN) {
            const imageSrc = webcamRef.current.getScreenshot();

            if (imageSrc) {
                ws.send(imageSrc.split(',')[1]); // Send only the base64 part of the data URL
            }
        }
    };

    return (
        <div className="container">
            <header>
                <img src={Logo} alt="Age Detection App Logo" className="logo" />
                <h1>Discover Your Age</h1>
                <p>Our advanced AI will guess your age from your webcam feed. Give it a try!</p>
            </header>
            <main>
                {/*{!isPredictionReceived ? (*/}
                    <div className="webcam-feed">
                        <Webcam
                            audio={false}
                            ref={webcamRef}
                            screenshotFormat="image/jpeg"
                            videoConstraints={{ width: 640, height: 480 }}
                        />
                    </div>
                {/*) : (*/}
                <div className="result-display">
                    {processedFrame && <img src={processedFrame} alt="Processed Frame" />}
                </div>
                    {/*)}*/}
            </main>
            <footer>
                <p>&copy; 2024 Age Detection App</p>
            </footer>
        </div>
    );
}

export default App;

