import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { PredictionListComponent } from './components/prediction-list/prediction-list.component';
import { InitDbComponent } from './components/init-db/init-db.component';
import { TrainModelComponent } from './components/train-model/train-model.component';

const routes: Routes = [
  { path: '', component: PredictionListComponent },
  { path: 'init-db', component: InitDbComponent },
  { path: 'train-model', component: TrainModelComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule {}
