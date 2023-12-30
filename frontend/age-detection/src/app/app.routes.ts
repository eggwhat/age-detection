import {RouterModule, Routes} from '@angular/router';
import {VideoUploadComponent} from "./video-upload/video-upload.component";
import {NgModule} from "@angular/core";

export const routes: Routes = [
  {path: 'video-upload', component: VideoUploadComponent},
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
