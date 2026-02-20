package com.example.backend.dto;

import java.util.List;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotEmpty;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class CreateMealRequest {
    
    @NotBlank(message = "Meal name is required")
    private String name;
    
    private String categoryName;
    private String areaName;
    private String instructions;
    private String thumbnailUrl;
    private String youtubeUrl;
    private String tags;
    
    @NotEmpty(message = "At least one ingredient is required")
    private List<IngredientRequest> ingredients;
    
    @Data
    @NoArgsConstructor
    @AllArgsConstructor
    public static class IngredientRequest {
        @NotBlank(message = "Ingredient name is required")
        private String name;
        
        @NotBlank(message = "Measure is required")
        private String measure;
    }
}
