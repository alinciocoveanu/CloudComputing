import { Component, OnInit } from '@angular/core';
import { AuthService } from '../services/auth.service';
import { AdvertService } from '../services/advert.service';
import { TILES } from '../components/grid-view/grid-view.variables';

@Component({
  selector: 'app-my-adverts',
  templateUrl: './my-adverts.component.html',
  styleUrls: ['./my-adverts.component.scss']
})
export class MyAdvertsComponent {
  loading = true;
  adverts = [];
  constructor(private authService: AuthService, private advertService: AdvertService) {
    this.authService.getDetails().then((info: any) => {
      this.advertService.getMyAdverts(info.user_id).then((rsp: any) => {
        rsp.reverse();
        let index = 0;
        rsp.forEach(advert => {
          advert.start_date = new Date(advert.start_date);
          advert.end_date = new Date(advert.end_date);
          this.adverts.push({ ...advert, tile: TILES[index] })
          index++;
          if (index == TILES.length) {
            index = 0;
          }
        });
      }, (err) => {
        console.log(err);
      }).finally(()=>{
        this.loading = false;
      })
    }, (err) => {
      console.log(err);
    })
  }

}
