import { Component, OnInit } from '@angular/core';
import {HttpClient, HttpParams} from '@angular/common/http';
import { HttpErrorResponse } from '@angular/common/http/src/response';
import { environment } from '../../environments/environment';

@Component({
  selector: 'app-sensor-chart',
  templateUrl: './sensor-chart.component.html',
  styleUrls: ['./sensor-chart.component.css']
})
export class SensorChartComponent  implements OnInit {
  private API_URL = environment.API_URL;
  multi: any[];
  sensors: any[];
  signals: any[];
  curSensor;
  startDate = '1990-01-01';
  endDate = '2018-01-01';
  selectedSignals;

  constructor (private httpService: HttpClient) { }


  ngOnInit(): void {
    this.getSensors();
  }
  view: any[] = [700, 400];

  showXAxis = true;
  showYAxis = true;
  gradient = false;
  showLegend = true;
  showXAxisLabel = true;
  xAxisLabel = 'Date';
  showYAxisLabel = true;
  yAxisLabel = 'Reading value';
  autoScale = true;

  colorScheme = {
    domain: ['#5AA454', '#A10A28', '#C7B42C', '#AAAAAA']
  };


  getSensors() {
    this.httpService.get(this.API_URL + '/sensors/')
      .subscribe(
        data => {
          this.sensors = data['sensors'];
          if (this.sensors) {
            this.setNewSensor(this.sensors[0]);
          }
          console.log(this.sensors);
        },
        (err: HttpErrorResponse) => {
          console.log (err.message);
        }
      );
  }

  getSignals(sensor) {
    this.httpService.get(this.API_URL + '/sensors/' + sensor)
      .subscribe(
        data => {
          this.signals = data['signals'];
          console.log(this.signals);
        },
        (err: HttpErrorResponse) => {
          console.log (err.message);
        }
      );
  }

  getData() {
    const params = {};
    params['signals'] = this.selectedSignals;
    params['start_date'] = this.startDate;
    params['end_date'] = this.endDate;
    this.httpService.get(this.API_URL + '/sensors/' + this.curSensor + '/readings', { params: params } )
      .subscribe(
      data => {
        console.log (data);
        this.multi = data['data'];
        console.log(this.multi);
      },
      (err: HttpErrorResponse) => {
        console.log (err.message);
      }
    );

  }

  setNewSensor(sensor) {
    this.curSensor = sensor;
    this.getSignals(this.curSensor);
  }

  change(options) {
    this.selectedSignals = Array.apply(null, options)
      .filter(option => option.selected)
      .map(option => option.value);
  }

  changeFrom($event) {
    this.startDate = $event.target.value;
  }

  changeTo($event) {
    this.endDate = $event.target.value;
  }
}
