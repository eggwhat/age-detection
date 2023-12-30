import * as faceapi from 'face-api.js';
import {AfterViewInit, Component, ElementRef, ViewChild} from "@angular/core";

@Component({
  selector: 'app-video-upload',
  templateUrl: './video-upload.component.html',
  styleUrls: ['./video-upload.component.css']
})
export class VideoUploadFaceApi implements AfterViewInit {
  @ViewChild('video', { static: true }) videoElement!: ElementRef<HTMLVideoElement>;
  @ViewChild('canvas', { static: true }) canvasElement!: ElementRef<HTMLCanvasElement>;

  video!: HTMLVideoElement;
  canvas!: HTMLCanvasElement;
  stream: MediaStream | null = null;

  ngAfterViewInit() {
    this.startCamera();
    this.loadModels();
  }

  startCamera() {
    navigator.mediaDevices.getUserMedia({ video: true })
      .then(stream => {
        this.stream = stream;
        this.video.srcObject = stream;
        this.video.play();
      })
      .catch(error => {
        console.error('Error accessing the camera:', error);
      });
  }

  async loadModels() {
    await faceapi.nets.tinyFaceDetector.loadFromUri('/models');
    await faceapi.nets.faceLandmark68Net.loadFromUri('/models');
    await faceapi.nets.faceRecognitionNet.loadFromUri('/models');
    await faceapi.nets.ageGenderNet.loadFromUri('/models');
  }

  async captureImage() {
    const detections = await faceapi.detectAllFaces(this.videoElement.nativeElement, new faceapi.TinyFaceDetectorOptions()).withAgeAndGender();

    this.drawDetections(detections);
  }

  drawDetections(detections: any[]) {
    const context = this.canvas.getContext('2d');
    if (context) {
      context.clearRect(0, 0, this.canvas.width, this.canvas.height);

      detections.forEach(detection => {
        const { x, y, width, height } = detection.detection.box;
        const age = detection.age;
        const text = `Age: ${Math.round(age)}`;

        context.strokeStyle = '#00FF00';
        context.lineWidth = 2;
        context.strokeRect(x, y, width, height);

        context.fillStyle = '#00FF00';
        context.font = '18px Arial';
        context.fillText(text, x, y - 5);
      });
    } else {
      console.error('Unable to get canvas context');
    }
  }

}

