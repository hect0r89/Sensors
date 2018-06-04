import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';
import { NgxChartsModule } from '@swimlane/ngx-charts';
import { AppRoutingModule } from './app-routing/app-routing.module';

import { AppComponent } from './app.component';
import { SensorComponent } from './sensor-upload/sensor.component';
import { SensorChartComponent } from './sensor-chart/sensor-chart.component';



@NgModule({
  declarations: [
    AppComponent,
    SensorComponent,
    SensorChartComponent,
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    NgxChartsModule,
    AppRoutingModule

  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
