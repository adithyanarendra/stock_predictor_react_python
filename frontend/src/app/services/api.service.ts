import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class ApiService {
  private baseUrl = 'http://127.0.0.1:5000';

  constructor(private http: HttpClient) {}

  initializeDb(): Observable<any> {
    console.log(this.http.get(`${this.baseUrl}/init_db`));
    
    return this.http.get(`${this.baseUrl}/init_db`);
  }

  trainModel(): Observable<any> {
    return this.http.get(`${this.baseUrl}/train_model`);
  }

  getPredictions(): Observable<any> {
    return this.http.get(`${this.baseUrl}/get_prediction`);
  }
}
