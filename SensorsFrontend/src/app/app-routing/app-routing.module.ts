import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { SensorComponent } from '../sensor-upload/sensor.component';
import { SensorChartComponent } from '../sensor-chart/sensor-chart.component';

export const appRoutes: Routes = [
  { path: '', component: SensorComponent },
  { path: 'stats', component: SensorChartComponent }
];
@NgModule({
  imports: [
    RouterModule.forRoot(
      appRoutes
    )
  ],
  exports: [
    RouterModule
  ]
})
export class AppRoutingModule {}
