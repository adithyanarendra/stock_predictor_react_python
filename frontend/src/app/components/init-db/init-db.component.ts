import { Component } from '@angular/core';
import { ApiService } from '../../services/api.service';
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
  selector: 'app-init-db',
  templateUrl: './init-db.component.html',
  styleUrls: ['./init-db.component.css'],
})
export class InitDbComponent {
  constructor(private apiService: ApiService, private snackBar: MatSnackBar) {}

  initDb(): void {
    this.apiService.initializeDb().subscribe({
      next: () => this.snackBar.open('Database initialized successfully!', 'Close', { duration: 3000 }),
      error: () => this.snackBar.open('Failed to initialize the database.', 'Close', { duration: 3000 }),
    });
  }
}
