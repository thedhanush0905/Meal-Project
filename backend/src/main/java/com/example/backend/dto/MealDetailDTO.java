package com.example.backend.dto;

import java.util.List;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class MealDetailDTO {
    private Long id;
    private Integer externalId;
    private String name;
    private String categoryName;
    private String areaName;
    private String instructions;
    private String thumbnailUrl;
    private String youtubeUrl;
    private String tags;
    private Boolean isExternal;
    private List<MealIngredientDTO> ingredients;
}
