package com.example.backend.service;

import com.example.backend.dto.*;
import com.example.backend.entity.*;
import com.example.backend.repository.*;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
@Slf4j
public class MealService {

    private final MealRepository mealRepository;
    private final CategoryRepository categoryRepository;
    private final AreaRepository areaRepository;
    private final IngredientRepository ingredientRepository;
    private final MealIngredientRepository mealIngredientRepository;

    /**
     * Get all meals for card view (id, name, thumbnail)
     */
    public List<MealCardDTO> getAllMealsForCards() {
        return mealRepository.findAll().stream()
                .map(meal -> new MealCardDTO(
                        meal.getId(),
                        meal.getName(),
                        meal.getThumbnailUrl()
                ))
                .collect(Collectors.toList());
    }

    /**
     * Get meal details by ID with full info and ingredients
     */
    public MealDetailDTO getMealDetails(Long id) {
        Meal meal = mealRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Meal not found with id: " + id));

        List<MealIngredientDTO> ingredients = mealIngredientRepository.findByMealId(id).stream()
                .map(mi -> new MealIngredientDTO(
                        mi.getIngredient().getId(),
                        mi.getIngredient().getName(),
                        mi.getMeasure()
                ))
                .collect(Collectors.toList());

        return new MealDetailDTO(
                meal.getId(),
                meal.getExternalId(),
                meal.getName(),
                meal.getCategory() != null ? meal.getCategory().getName() : null,
                meal.getArea() != null ? meal.getArea().getName() : null,
                meal.getInstructions(),
                meal.getThumbnailUrl(),
                meal.getYoutubeUrl(),
                meal.getTags(),
                meal.getIsExternal(),
                ingredients
        );
    }

    /**
     * Filter meals by category
     */
    public List<MealCardDTO> getMealsByCategory(String categoryName) {
        Category category = categoryRepository.findByName(categoryName)
                .orElseThrow(() -> new RuntimeException("Category not found: " + categoryName));

        return mealRepository.findByCategoryId(category.getId()).stream()
                .map(meal -> new MealCardDTO(
                        meal.getId(),
                        meal.getName(),
                        meal.getThumbnailUrl()
                ))
                .collect(Collectors.toList());
    }

    /**
     * Filter meals by ingredient using JPQL
     */
    public List<MealCardDTO> getMealsByIngredient(String ingredientName) {
        Ingredient ingredient = ingredientRepository.findByName(ingredientName)
                .orElseThrow(() -> new RuntimeException("Ingredient not found: " + ingredientName));

        return mealIngredientRepository.findByIngredientId(ingredient.getId()).stream()
                .map(mi -> new MealCardDTO(
                        mi.getMeal().getId(),
                        mi.getMeal().getName(),
                        mi.getMeal().getThumbnailUrl()
                ))
                .collect(Collectors.toList());
    }

    /**
     * Search meals by name (case-insensitive, partial match)
     */
    public List<MealCardDTO> searchMealsByName(String name) {
        return mealRepository.findByNameContainingIgnoreCase(name).stream()
                .map(meal -> new MealCardDTO(
                        meal.getId(),
                        meal.getName(),
                        meal.getThumbnailUrl()
                ))
                .collect(Collectors.toList());
    }

    /**
     * Create a new user meal
     */
    @Transactional
    public MealDetailDTO createUserMeal(CreateMealRequest request) {
        log.info("Creating user meal: {}", request.getName());

        // Get or create category
        Category category = null;
        if (request.getCategoryName() != null && !request.getCategoryName().trim().isEmpty()) {
            category = categoryRepository.findByName(request.getCategoryName())
                    .orElseGet(() -> {
                        Category newCategory = new Category();
                        newCategory.setName(request.getCategoryName());
                        return categoryRepository.save(newCategory);
                    });
        }

        // Get or create area
        Area area = null;
        if (request.getAreaName() != null && !request.getAreaName().trim().isEmpty()) {
            area = areaRepository.findByName(request.getAreaName())
                    .orElseGet(() -> {
                        Area newArea = new Area();
                        newArea.setName(request.getAreaName());
                        return areaRepository.save(newArea);
                    });
        }

        // Create meal
        Meal meal = new Meal();
        meal.setName(request.getName());
        meal.setCategory(category);
        meal.setArea(area);
        meal.setInstructions(request.getInstructions());
        meal.setThumbnailUrl(request.getThumbnailUrl());
        meal.setYoutubeUrl(request.getYoutubeUrl());
        meal.setTags(request.getTags());
        meal.setIsExternal(false); // User-created meal
        meal.setExternalId(null);
        meal.setCreatedBy(null); // TODO: Set this when user auth is implemented

        meal = mealRepository.save(meal);
        log.info("Saved meal with id: {}", meal.getId());

        // Save ingredients
        for (CreateMealRequest.IngredientRequest ingredientReq : request.getIngredients()) {
            Ingredient ingredient = ingredientRepository.findByName(ingredientReq.getName())
                    .orElseGet(() -> {
                        Ingredient newIngredient = new Ingredient();
                        newIngredient.setName(ingredientReq.getName());
                        return ingredientRepository.save(newIngredient);
                    });

            MealIngredient mealIngredient = new MealIngredient();
            mealIngredient.setMeal(meal);
            mealIngredient.setIngredient(ingredient);
            mealIngredient.setMeasure(ingredientReq.getMeasure());
            mealIngredientRepository.save(mealIngredient);
        }

        // Return the created meal details
        return getMealDetails(meal.getId());
    }

    /**
     * Get all categories
     */
    public List<String> getAllCategories() {
        return categoryRepository.findAll().stream()
                .map(Category::getName)
                .collect(Collectors.toList());
    }

    /**
     * Get all areas
     */
    public List<String> getAllAreas() {
        return areaRepository.findAll().stream()
                .map(Area::getName)
                .collect(Collectors.toList());
    }

    /**
     * Get all ingredients
     */
    public List<String> getAllIngredients() {
        return ingredientRepository.findAll().stream()
                .map(Ingredient::getName)
                .collect(Collectors.toList());
    }
}
