export const captureAndSendFrame = (webcamRef, ws) => {
    if (webcamRef.current && ws?.readyState === WebSocket.OPEN) {
        const imageSrc = webcamRef.current.getScreenshot();

        if (imageSrc) {
            ws.send(imageSrc.split(',')[1]);
        }
    }
};

export const handleFileSelect = (event) => {
    const files = [...event.target.files];
    handleImageUpload(files);
};

export const handleImageUpload = async (files) => {

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


export const handleVideoUpload = async (file, setIsLoading, setIsWebcamActive) => {
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
