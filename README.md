# Age Detection App User Manual

## Version 1.0

## Table of Contents
1. [Introduction](#introduction)
2. [System Requirements](#system-requirements)
3. [Installation Guide](#installation-guide)
4. [Getting Started](#getting-started)
5. [Uploading an Image](#uploading-an-image)
6. [Uploading a Video](#uploading-a-video)
7. [Troubleshooting](#troubleshooting)
8. [Contact Information](#contact-information)

---

### Introduction
Welcome to the Age Detection App! Our advanced AI technology estimates the age of individuals from photos and videos. This manual will guide you through the process of installing and using the application.

### System Requirements
- Operating System: Windows 10, MacOS 10.14, or any modern Linux distribution
- Browser: Latest versions of Chrome, Firefox, or Safari
- Webcam: Required if using live feed features
- Python 3.9 or higher
- Node.js 12 or higher

### Installation Guide


To ensure proper installation of the Age Detection App, follow these steps:

1. **Clone the Repository**: https://github.com/grioool/human-age-detection
2. **Set Up Python Environment**:
   - Ensure Python 3.9+ is installed.
   - Set up a virtual environment: `python -m venv venv`
   - Activate the virtual environment: `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows)
   - Navigate in terminal to /backend
   - Install the required Python libraries: `pip install -r requirements.txt`
   - To run in the /backend folder run: uvicorn api:app
3. **Set Up React Environment**:
   - Ensure Node.js 12+ is installed.
   - Navigate in terminal to /frontend/age-detection/
   - Install dependencies: `npm install`
   - To run in the /frontend/age-detection/ run: npm start
   - App will be hosted on http://localhost:3000

### Getting Started
1. **Launch the App**: Open the installed application or navigate to the web address: Local: http://localhost:3000 On Your Network:  http://<local-ip>:3000.
2. **Grant Permissions**: Allow the application to access your webcam if prompted.

### Uploading an Image
1. **Navigate to the Image Section**: Click on the ‘Upload Image’ button.
2. **Choose a Directory**: Click the button and select directory. Ensure the images in directory are clear and the face(s) is/are visible.
3. **Upload and Analyze**: Once the directory is selected, the app will automatically upload and analyze the images to estimate the age of the individuals present and save them to archive

### Uploading a Video
1. **Navigate to the Video Section**: Click on the 'Upload Video' button if you wish to use a pre-recorded video.
2. **Choose a Video File**: A dialog will appear for you to select a video file from your computer.
3. **Upload and Analyze**: After selecting the file, the application will process, save the video and display the estimated age for the individuals in the video.

### Using the Webcam 
1. **Webcam Feed**: You may be prompted to enable your webcam.
2. **Real-Time Analysis**: The app will provide real-time age estimations based on the webcam feed.

### Troubleshooting
- **Webcam Not Detected**: Ensure your webcam drivers are up to date and that the webcam is not being used by another application.
- **Upload Failures**: Check your internet connection and ensure the file size does not exceed the maximum limit.
- **Inaccurate Age Estimation**: Ensure the image or video is clear and the subject's face is not obstructed.

### Contact Information
For any technical support or queries, please reach out to:

- **Support Email**: olga.a.grigorieva@gmail.com
