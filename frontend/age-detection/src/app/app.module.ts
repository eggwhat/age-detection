import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { SocketIoModule, SocketIoConfig } from 'ngx-socket-io';
import { AppComponent } from './app.component';
import { WebSocketService } from './websocket.service';
import {VideoUploadComponent} from "./video-upload/video-upload.component";
import {VideoUploadFaceApi} from "./video-upload/video-upload-face-api";

const config: SocketIoConfig = { url: 'YOUR_WEBSOCKET_SERVER_URL', options: {} };

@NgModule({
  declarations: [
    VideoUploadComponent,
    VideoUploadFaceApi
  ],
  imports: [BrowserModule, SocketIoModule.forRoot(config)],
  providers: [WebSocketService],
  bootstrap: [AppComponent]
})
export class AppModule {}
