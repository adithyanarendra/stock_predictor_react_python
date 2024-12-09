import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';

// Import Angular Material modules
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatTableModule } from '@angular/material/table';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';

@NgModule({
  declarations: [
    AppComponent
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule, // Required for Angular Material animations
    AppRoutingModule,
    MatToolbarModule,         // Import Material Toolbar Module
    MatButtonModule,          // Import Material Button Module
    MatCardModule,            // Import Material Card Module
    MatTableModule,           // Import Material Table Module
    MatProgressSpinnerModule  // Import Material Progress Spinner
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
