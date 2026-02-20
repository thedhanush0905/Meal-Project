package com.example.backend.controller;

import com.example.backend.dto.CreateMealRequest;
import com.example.backend.dto.MealCardDTO;
import com.example.backend.dto.MealDetailDTO;
import com.example.backend.service.MealService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/meals")
@RequiredArgsConstructor
@CrossOrigin(origins = "*")
public class MealController {

    private final MealService mealService;

    /**
     * Get all categories
     * GET /api/meals/categories
     * NOTE: This must be BEFORE /{id} to avoid routing conflicts
     */
    @GetMapping("/categories")
    public ResponseEntity<List<String>> getAllCategories() {
        return ResponseEntity.ok(mealService.getAllCategories());
    }

    /**
     * Get all areas
     * GET /api/meals/areas
     */
    @GetMapping("/areas")
    public ResponseEntity<List<String>> getAllAreas() {
        return ResponseEntity.ok(mealService.getAllAreas());
    }

    /**
     * Get all ingredients
     * GET /api/meals/ingredients
     */
    @GetMapping("/ingredients")
    public ResponseEntity<List<String>> getAllIngredients() {
        return ResponseEntity.ok(mealService.getAllIngredients());
    }

    /**
     * Search meals by name
     * GET /api/meals/search?name=chicken
     */
    @GetMapping("/search")
    public ResponseEntity<List<MealCardDTO>> searchMealsByName(@RequestParam String name) {
        List<MealCardDTO> meals = mealService.searchMealsByName(name);
        return ResponseEntity.ok(meals);
    }

    /**
     * Task 5.1 - Get all meals for card view
     * GET /api/meals
     */
    @GetMapping
    public ResponseEntity<List<MealCardDTO>> getAllMeals(
            @RequestParam(required = false) String category,
            @RequestParam(required = false) String ingredient) {
        
        List<MealCardDTO> meals;
        
        if (category != null && !category.trim().isEmpty()) {
            // Task 5.3 - Filter by category
            meals = mealService.getMealsByCategory(category);
        } else if (ingredient != null && !ingredient.trim().isEmpty()) {
            // Task 5.4 - Filter by ingredient
            meals = mealService.getMealsByIngredient(ingredient);
        } else {
            // Get all meals
            meals = mealService.getAllMealsForCards();
        }
        
        return ResponseEntity.ok(meals);
    }

    /**
     * Task 5.2 - Get meal details by ID
     * GET /api/meals/{id}
     * NOTE: This must be AFTER specific paths like /categories, /areas, /ingredients
     */
    @GetMapping("/{id}")
    public ResponseEntity<MealDetailDTO> getMealDetails(@PathVariable Long id) {
        MealDetailDTO meal = mealService.getMealDetails(id);
        return ResponseEntity.ok(meal);
    }

    /**
     * Task 5.5 - Add user meal
     * POST /api/meals
     */
    @PostMapping
    public ResponseEntity<MealDetailDTO> createMeal(@Valid @RequestBody CreateMealRequest request) {
        MealDetailDTO createdMeal = mealService.createUserMeal(request);
        return ResponseEntity.status(HttpStatus.CREATED).body(createdMeal);
    }
}
