import {Component, OnInit} from '@angular/core';
import {RecipeService} from "../recipe.service";
import {CommentModalComponent} from "../recipe-detail/comment-modal/comment-modal.component";
import {AddAllergenModalComponent} from "./allergens/add-allergen-modal/add-allergen-modal.component";
import {NgbModal} from "@ng-bootstrap/ng-bootstrap";
import {ToastrService} from "ngx-toastr";
import {DeleteModalComponent} from "./delete-modal/delete-modal.component";

@Component({
  selector: 'app-new-recipe',
  templateUrl: './new-recipe.component.html',
  styleUrls: ['./new-recipe.component.scss']
})
export class NewRecipeComponent implements OnInit {

  public categories: any;
  public cuisine: any;
  public courses: any;

  public loadingCategory = true;
  public loadingCuisine = true;
  public loadingCourses = true;


  constructor(private recipeService: RecipeService,
              private modalService: NgbModal,
              private toastr: ToastrService) {
  }

  ngOnInit() {

    this.recipeService.getCategories().subscribe(categories => {
      this.categories = categories;
      this.loadingCategory = false;
    });
    this.recipeService.getCuisines().subscribe(cuisine => {
      this.cuisine = cuisine;
      this.loadingCuisine = false;
    });
    this.recipeService.getCourses().subscribe(courses => {
      this.courses = courses;
      this.loadingCourses = true;
    });
  }




}
