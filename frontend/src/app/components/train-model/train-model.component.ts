import { Component } from '@angular/core';
import { ApiService } from '../../services/api.service';
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
  selector: 'app-train-model',
  templateUrl: './train-model.component.html',
  styleUrls: ['./train-model.component.css'],
})
export class TrainModelComponent {
  constructor(private apiService: ApiService, private snackBar: MatSnackBar) {}

  trainModel(): void {
    this.apiService.trainModel().subscribe({
      next: () => this.snackBar.open('Model trained successfully!', 'Close', { duration: 3000 }),
      error: () => this.snackBar.open('Failed to train the model.', 'Close', { duration: 3000 }),
    });
  }
}
