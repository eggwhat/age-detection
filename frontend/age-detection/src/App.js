import React, {useEffect, useRef, useState} from 'react';
import Webcam from 'react-webcam';
import Logo from './assets/logo.svg';
import './styles/App.css';
import {Loader} from "./components/Loader/Loader";
import {captureAndSendFrame, handleImageUpload, handleVideoUpload} from "./service/MediaUploader";
import {MediaInput} from "./components/MediaInput/MediaInput";

function App() {
    const webcamRef = useRef(null);
    const [ws, setWs] = useState(null);
    const [processedFrame, setProcessedFrame] = useState(null);
    const [isPredictionReceived, setIsPredictionReceived] = useState(false);
    const [isLoading, setIsLoading] = useState(false);
    const [isWebcamActive, setIsWebcamActive] = useState(true);

    useEffect(() => {
        const websocket = new WebSocket('ws://127.0.0.1:8000/detect-age/ws');
        setWs(websocket)

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
                captureAndSendFrame(webcamRef, ws);
            }, 1000 / 10);

            return () => clearInterval(interval);
        }
    }, [ws]);


    return (
        <div className="container">
            <header>
                <img src={Logo} alt="Age Detection App Logo" className="logo"/>
                <h1>Discover Your Age</h1>
                <p>Our advanced AI will guess your age from your webcam feed. Give it a try!</p>
            </header>
            <main>
                <div className="button-container">
                    <MediaInput directory={true} text={"Upload Image Directory"} multiple={true} accept={"image"}
                                onChange={(e) => handleImageUpload([...e.target.files], setIsLoading, setIsWebcamActive)}
                                id={"imageUploadDir"}/>
                    <MediaInput directory={false} text={"Upload Video"} multiple={false} accept={"video"}
                                onChange={(e) => handleVideoUpload(e.target.files[0], setIsLoading, setIsWebcamActive)}
                                id={"videoUpload"}/>
                </div>

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