import { Component, OnInit } from '@angular/core';
import { ApiService } from '../../services/api.service';

@Component({
  selector: 'app-prediction-list',
  templateUrl: './prediction-list.component.html',
  styleUrls: ['./prediction-list.component.css'],
})
export class PredictionListComponent implements OnInit {
  predictions: any[] = [];
  displayedColumns: string[] = ['stock_symbol', 'timestamp', 'actual_price', 'predicted_price', 'accuracy'];
  loading = true;

  constructor(private apiService: ApiService) {}

  ngOnInit(): void {
    this.apiService.getPredictions().subscribe({
      next: (data) => {
        this.predictions = data;
        this.loading = false;
      },
      error: (err) => {
        console.error('Error fetching predictions:', err);
        this.loading = false;
      },
    });
  }
}
