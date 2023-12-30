import { Injectable } from '@angular/core';
import { Observable, Subject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class WebsocketService {
  private websocket!: WebSocket;
  private incomingMessage: Subject<string> = new Subject();

  constructor() {
    this.connect();
  }

  private connect(): void {
    this.websocket = new WebSocket('ws://localhost:8000/detect-age/ws');

    this.websocket.onmessage = (event) => {
      this.incomingMessage.next(event.data);
    };
  }

  sendMessage(message: string): void {
    this.websocket.send(message);
  }

  getMessages(): Observable<string> {
    return this.incomingMessage.asObservable();
  }

}
