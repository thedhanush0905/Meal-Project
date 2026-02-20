package com.example.backend.service;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;
import com.example.backend.dto.IngredientCalorie;
import com.example.backend.dto.CalorieResponse;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

@Service
public class MealService {
    
    private final WebClient webClient;
    
    @Value("${nutrition.api.url:https://api.api-ninjas.com/v1/nutrition}")
    private String nutritionApiUrl;
    
    @Value("${nutrition.api.key:}")
    private String nutritionApiKey;
    
    public MealService(WebClient.Builder webClientBuilder) {
        this.webClient = webClientBuilder.build();
    }
    
    @SuppressWarnings("unchecked")
    public List<Map<String, Object>> searchMeals(String query) {
        String url = "https://www.themealdb.com/api/json/v1/1/search.php?s=" + query;
        
        Map<String, Object> response = webClient.get()
                .uri(url)
                .retrieve()
                .bodyToMono(Map.class)
                .block();
        
        if (response != null && response.containsKey("meals")) {
            Object meals = response.get("meals");
            if (meals instanceof List) {
                return (List<Map<String, Object>>) meals;
            }
        }
        return new ArrayList<>();
    }
    
    @SuppressWarnings("unchecked")
    public Map<String, Object> getMealById(String id) {
        String url = "https://www.themealdb.com/api/json/v1/1/lookup.php?i=" + id;
        
        Map<String, Object> response = webClient.get()
                .uri(url)
                .retrieve()
                .bodyToMono(Map.class)
                .block();
        
        if (response != null && response.containsKey("meals")) {
            List<Map<String, Object>> meals = (List<Map<String, Object>>) response.get("meals");
            if (meals != null && !meals.isEmpty()) {
                return meals.get(0);
            }
        }
        return null;
    }
    
    public CalorieResponse calculateCalories(String mealId) {
        Map<String, Object> meal = getMealById(mealId);
        
        if (meal == null) {
            throw new RuntimeException("Meal not found with id: " + mealId);
        }
        
        String mealName = (String) meal.get("strMeal");
        List<IngredientCalorie> ingredients = new ArrayList<>();
        double totalCalories = 0;
        
        // Extract ingredients and measures (TheMealDB has up to 20 ingredients)
        for (int i = 1; i <= 20; i++) {
            String ingredient = (String) meal.get("strIngredient" + i);
            String measure = (String) meal.get("strMeasure" + i);
            
            if (ingredient != null && !ingredient.trim().isEmpty()) {
                double calories = getCaloriesFromNutritionAPI(ingredient, measure);
                ingredients.add(new IngredientCalorie(ingredient, measure != null ? measure : "", calories));
                totalCalories += calories;
            }
        }
        
        return new CalorieResponse(mealId, mealName, ingredients, Math.round(totalCalories * 100.0) / 100.0);
    }
    
    @SuppressWarnings("unchecked")
    private double getCaloriesFromNutritionAPI(String ingredient, String measure) {
        try {
            String query = ingredient;
            if (measure != null && !measure.trim().isEmpty()) {
                query = measure + " " + ingredient;
            }
            
            List<Map<String, Object>> nutritionData = webClient.get()
                    .uri(nutritionApiUrl + "?query=" + query)
                    .header("X-Api-Key", nutritionApiKey)
                    .retrieve()
                    .bodyToMono(List.class)
                    .block();
            
            if (nutritionData != null && !nutritionData.isEmpty()) {
                Object caloriesObj = nutritionData.get(0).get("calories");
                if (caloriesObj instanceof Number) {
                    return ((Number) caloriesObj).doubleValue();
                }
            }
        } catch (Exception e) {
            System.err.println("Error fetching calories for " + ingredient + ": " + e.getMessage());
        }
        
        // Return default if API fails
        return 0.0;
    }
    
    public Map<String, Object> findLeastIngredientsMeal(String query) {
        List<Map<String, Object>> meals = searchMeals(query);
        
        if (meals.isEmpty()) {
            return null;
        }
        
        Map<String, Object> leastIngredientMeal = meals.get(0);
        int minIngredients = countIngredients(leastIngredientMeal);
        
        for (Map<String, Object> meal : meals) {
            int count = countIngredients(meal);
            if (count < minIngredients) {
                minIngredients = count;
                leastIngredientMeal = meal;
            }
        }
        
        return leastIngredientMeal;
    }
    
    private int countIngredients(Map<String, Object> meal) {
        int count = 0;
        for (int i = 1; i <= 20; i++) {
            String ingredient = (String) meal.get("strIngredient" + i);
            if (ingredient != null && !ingredient.trim().isEmpty()) {
                count++;
            }
        }
        return count;
    }
}
