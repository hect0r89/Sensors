import { Component, OnInit } from '@angular/core';
import {HttpClient} from '@angular/common/http';
import { HttpErrorResponse } from '@angular/common/http/src/response';
import { environment } from '../../environments/environment';

@Component({
  selector: 'app-sensor',
  templateUrl: './sensor.component.html',
  styleUrls: ['./sensor.component.css']
})
export class SensorComponent {
  is_loading = 'none';
  private API_URL = environment.API_URL;

  constructor (private httpService: HttpClient) {}

  myFiles: string [] = [];
  sMsg = '';

  getFileDetails (e) {
    this.myFiles = [];
    for (let i = 0; i < e.target.files.length; i++) {
      this.myFiles.push(e.target.files[i]);
    }
  }

  uploadFiles () {
    this.is_loading = 'block';
    const frmData = new FormData();
    for (let i = 0; i < this.myFiles.length; i++) {
      frmData.append('files', this.myFiles[i]);
    }
    this.httpService.post(this.API_URL + '/upload/', frmData).subscribe(
      data => {
        this.sMsg = data as string;
        console.log (this.sMsg);
        this.is_loading = 'none';
      },
      (err: HttpErrorResponse) => {
        console.log (err.message);
        this.is_loading = 'none';
      }
    );
  }
}
