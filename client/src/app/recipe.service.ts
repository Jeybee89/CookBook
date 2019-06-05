import { Injectable } from '@angular/core';
import {HttpClient} from '@angular/common/http';


@Injectable({
  providedIn: 'root'
})
export class RecipeService {

  url = 'http://127.0.0.1:5000';

  constructor(private http: HttpClient) { }

   getRecipes() {
    return this.http.get(`${this.url}/recipes`);
  }
  getRecipe(id) {
    return this.http.get(`${this.url}/recipe/` + id );
  }
}
