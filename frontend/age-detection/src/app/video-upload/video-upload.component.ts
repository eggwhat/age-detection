import {Component, ElementRef, ViewChild, OnDestroy, OnInit} from '@angular/core';
import {WebsocketService} from "../websocket.service";
import {ImageProcessingService} from "../image-processing.service";

@Component({
  selector: 'app-video-upload',
  templateUrl: './video-upload.component.html',
  styleUrls: ['./video-upload.component.css']
})
export class VideoUploadComponent implements OnDestroy, OnInit {
  @ViewChild('video', { static: true }) videoElement!: ElementRef<HTMLVideoElement>;
  @ViewChild('canvas', { static: true }) canvasElement!: ElementRef<HTMLCanvasElement>;

  video!: HTMLVideoElement;
  canvas!: HTMLCanvasElement;
  stream: MediaStream | null = null;
  agePrediction: string = '';

  constructor(private websocketService: WebsocketService, private imageService:ImageProcessingService) {
    this.websocketService.getMessages().subscribe((processedImageData) => {
      console.log('Received processed image data:', processedImageData);
    });
  }

  ngOnInit() {
    this.video = this.videoElement.nativeElement;
    this.canvas = this.canvasElement.nativeElement;
    this.startCamera();
  }

  ngOnDestroy(): void {
    if (this.stream) {
      this.stream.getTracks().forEach(track => track.stop());
    }
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

  captureImage() {
    const context = this.canvas.getContext('2d');
    if (context) {
      context.drawImage(this.video, 0, 0, this.canvas.width, this.canvas.height);
      const imageData = this.canvas.toDataURL('image/png');
      this.websocketService.sendMessage(imageData);
    } else {
      console.error('Unable to get canvas context');
    }
  }

  predictAge(imageData: string) {
    this.imageService.predictAge(imageData).subscribe(response => {
      this.agePrediction = `Predicted Age: ${response.age} years`;
    }, error => {
      console.error('Error predicting age:', error);
    });
  }

}
