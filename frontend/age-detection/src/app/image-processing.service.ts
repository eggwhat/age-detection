import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class ImageProcessingService {
  private apiUrl = 'ws://localhost:8000/detect-age/ws';

  constructor(private http: HttpClient) {}

  predictAge(imageData: string) {
    return this.http.post<any>(`${this.apiUrl}/predict-age`, { image: imageData });
  }

  uploadImageAndReceiveZip(file: File) {
    const formData = new FormData();
    formData.append('file', file);
    return this.http.post(`${this.apiUrl}/predict-age`, formData, { responseType: 'blob' });
  }

  uploadVideoAndReceiveProcessed(file: File) {
    const formData = new FormData();
    formData.append('file', file);
    return this.http.post(`${this.apiUrl}/predict-age`, formData, { responseType: 'blob' });
  }

}
