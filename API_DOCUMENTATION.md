# Meal Project - Backend API Documentation

## Base URL
```
http://localhost:8082/api
```

---

## 📋 Table of Contents
1. [Get All Meals](#1-get-all-meals)
2. [Get Meal Details by ID](#2-get-meal-details-by-id)
3. [Search Meals by Name](#3-search-meals-by-name)
4. [Filter Meals by Category](#4-filter-meals-by-category)
5. [Filter Meals by Ingredient](#5-filter-meals-by-ingredient)
6. [Create User Meal](#6-create-user-meal)
7. [Get All Categories](#7-get-all-categories)
8. [Get All Areas](#8-get-all-areas)
9. [Get All Ingredients](#9-get-all-ingredients)

---

## 1. Get All Meals

Get all meals with basic information (card view).

**Endpoint:** `GET /meals`

**Response:**
```json
[
  {
    "id": 1,
    "name": "Chicken Curry",
    "thumbnailUrl": "https://www.themealdb.com/images/media/meals/1548772327.jpg"
  },
  {
    "id": 2,
    "name": "Spaghetti Carbonara",
    "thumbnailUrl": "https://www.themealdb.com/images/media/meals/1520531635.jpg"
  }
]
```

**Example:**
```javascript
fetch('http://localhost:8082/api/meals')
  .then(response => response.json())
  .then(data => console.log(data));
```

---

## 2. Get Meal Details by ID

Get complete details of a specific meal including ingredients.

**Endpoint:** `GET /meals/{id}`

**Path Parameters:**
- `id` (Long) - Meal ID

**Response:**
```json
{
  "id": 1,
  "externalId": 52940,
  "name": "Brown Stew Chicken",
  "categoryName": "Chicken",
  "areaName": "Jamaican",
  "instructions": "Squeeze lime over chicken and rub well...",
  "thumbnailUrl": "https://www.themealdb.com/images/media/meals/sypxpx1515365095.jpg",
  "youtubeUrl": "https://www.youtube.com/watch?v=...",
  "tags": "Stew,Chicken",
  "isExternal": true,
  "ingredients": [
    {
      "ingredientId": 15,
      "ingredientName": "Chicken",
      "measure": "2 lbs"
    },
    {
      "ingredientId": 23,
      "ingredientName": "Onion",
      "measure": "1 chopped"
    }
  ]
}
```

**Example:**
```javascript
fetch('http://localhost:8082/api/meals/1')
  .then(response => response.json())
  .then(data => console.log(data));
```

---

## 3. Search Meals by Name

Search for meals by name (case-insensitive, partial match).

**Endpoint:** `GET /meals/search`

**Query Parameters:**
- `name` (String, required) - Search term

**Response:**
```json
[
  {
    "id": 5,
    "name": "Chicken Curry",
    "thumbnailUrl": "https://..."
  },
  {
    "id": 12,
    "name": "Teriyaki Chicken",
    "thumbnailUrl": "https://..."
  }
]
```

**Example:**
```javascript
fetch('http://localhost:8082/api/meals/search?name=chicken')
  .then(response => response.json())
  .then(data => console.log(data));
```

---

## 4. Filter Meals by Category

Get all meals from a specific category.

**Endpoint:** `GET /meals?category={categoryName}`

**Query Parameters:**
- `category` (String, required) - Category name (e.g., "Seafood", "Vegetarian", "Chicken")

**Response:**
```json
[
  {
    "id": 10,
    "name": "Salmon Teriyaki",
    "thumbnailUrl": "https://..."
  },
  {
    "id": 15,
    "name": "Fish and Chips",
    "thumbnailUrl": "https://..."
  }
]
```

**Example:**
```javascript
fetch('http://localhost:8082/api/meals?category=Seafood')
  .then(response => response.json())
  .then(data => console.log(data));
```

---

## 5. Filter Meals by Ingredient

Get all meals that contain a specific ingredient.

**Endpoint:** `GET /meals?ingredient={ingredientName}`

**Query Parameters:**
- `ingredient` (String, required) - Ingredient name (e.g., "Chicken", "Tomato", "Garlic")

**Response:**
```json
[
  {
    "id": 3,
    "name": "Spaghetti Bolognese",
    "thumbnailUrl": "https://..."
  },
  {
    "id": 8,
    "name": "Tomato Soup",
    "thumbnailUrl": "https://..."
  }
]
```

**Example:**
```javascript
fetch('http://localhost:8082/api/meals?ingredient=Tomato')
  .then(response => response.json())
  .then(data => console.log(data));
```

---

## 6. Create User Meal

Create a new custom meal with ingredients.

**Endpoint:** `POST /meals`

**Request Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "name": "My Special Pasta",
  "categoryName": "Pasta",
  "areaName": "Italian",
  "instructions": "1. Boil water\n2. Add pasta\n3. Cook for 10 minutes...",
  "thumbnailUrl": "https://example.com/image.jpg",
  "youtubeUrl": "https://youtube.com/watch?v=...",
  "tags": "Pasta,Italian,Quick",
  "ingredients": [
    {
      "name": "Pasta",
      "measure": "500g"
    },
    {
      "name": "Tomato Sauce",
      "measure": "2 cups"
    },
    {
      "name": "Garlic",
      "measure": "3 cloves"
    }
  ]
}
```

**Required Fields:**
- `name` (String) - Meal name
- `ingredients` (Array) - At least one ingredient
  - Each ingredient must have:
    - `name` (String) - Ingredient name
    - `measure` (String) - Measurement (e.g., "2 cups", "100g")

**Optional Fields:**
- `categoryName` (String)
- `areaName` (String)
- `instructions` (String)
- `thumbnailUrl` (String)
- `youtubeUrl` (String)
- `tags` (String)

**Response:** (Status: 201 Created)
```json
{
  "id": 596,
  "externalId": null,
  "name": "My Special Pasta",
  "categoryName": "Pasta",
  "areaName": "Italian",
  "instructions": "1. Boil water\n2. Add pasta\n3. Cook for 10 minutes...",
  "thumbnailUrl": "https://example.com/image.jpg",
  "youtubeUrl": "https://youtube.com/watch?v=...",
  "tags": "Pasta,Italian,Quick",
  "isExternal": false,
  "ingredients": [
    {
      "ingredientId": 45,
      "ingredientName": "Pasta",
      "measure": "500g"
    },
    {
      "ingredientId": 67,
      "ingredientName": "Tomato Sauce",
      "measure": "2 cups"
    },
    {
      "ingredientId": 23,
      "ingredientName": "Garlic",
      "measure": "3 cloves"
    }
  ]
}
```

**Example:**
```javascript
fetch('http://localhost:8082/api/meals', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    name: 'My Special Pasta',
    categoryName: 'Pasta',
    areaName: 'Italian',
    instructions: '1. Boil water\n2. Add pasta...',
    thumbnailUrl: 'https://example.com/image.jpg',
    ingredients: [
      { name: 'Pasta', measure: '500g' },
      { name: 'Tomato Sauce', measure: '2 cups' }
    ]
  })
})
  .then(response => response.json())
  .then(data => console.log(data));
```

**Validation Errors:** (Status: 400 Bad Request)
```json
{
  "timestamp": "2026-02-20T10:30:00.000Z",
  "status": 400,
  "error": "Bad Request",
  "message": "Validation failed",
  "errors": {
    "name": "Meal name is required",
    "ingredients": "At least one ingredient is required"
  }
}
```

---

## 7. Get All Categories

Get a list of all available meal categories.

**Endpoint:** `GET /meals/categories`

**Response:**
```json
[
  "Beef",
  "Chicken",
  "Dessert",
  "Lamb",
  "Miscellaneous",
  "Pasta",
  "Pork",
  "Seafood",
  "Side",
  "Starter",
  "Vegan",
  "Vegetarian",
  "Breakfast",
  "Goat"
]
```

**Example:**
```javascript
fetch('http://localhost:8082/api/meals/categories')
  .then(response => response.json())
  .then(data => console.log(data));
```

---

## 8. Get All Areas

Get a list of all available meal origin areas/cuisines.

**Endpoint:** `GET /meals/areas`

**Response:**
```json
[
  "American",
  "British",
  "Canadian",
  "Chinese",
  "Croatian",
  "Dutch",
  "Egyptian",
  "French",
  "Greek",
  "Indian",
  "Irish",
  "Italian",
  "Jamaican",
  "Japanese",
  "Kenyan",
  "Malaysian",
  "Mexican",
  "Moroccan",
  "Polish",
  "Portuguese",
  "Russian",
  "Spanish",
  "Thai",
  "Tunisian",
  "Turkish",
  "Vietnamese"
]
```

**Example:**
```javascript
fetch('http://localhost:8082/api/meals/areas')
  .then(response => response.json())
  .then(data => console.log(data));
```

---

## 9. Get All Ingredients

Get a list of all available ingredients in the database.

**Endpoint:** `GET /meals/ingredients`

**Response:**
```json
[
  "Chicken",
  "Salt",
  "Olive Oil",
  "Onion",
  "Tomato",
  "Garlic",
  "Pasta",
  "Rice",
  "...hundreds more..."
]
```

**Example:**
```javascript
fetch('http://localhost:8082/api/meals/ingredients')
  .then(response => response.json())
  .then(data => console.log(data));
```

---

## 🔧 Common HTTP Status Codes

| Code | Description |
|------|-------------|
| 200 | OK - Request successful |
| 201 | Created - Resource created successfully |
| 400 | Bad Request - Invalid request data or validation error |
| 404 | Not Found - Resource not found |
| 500 | Internal Server Error - Server error |

---

## 🚀 Quick Start Example (React)

```javascript
// Get all meals
const fetchMeals = async () => {
  try {
    const response = await fetch('http://localhost:8082/api/meals');
    const meals = await response.json();
    console.log(meals);
  } catch (error) {
    console.error('Error fetching meals:', error);
  }
};

// Get meal details
const fetchMealDetails = async (mealId) => {
  try {
    const response = await fetch(`http://localhost:8082/api/meals/${mealId}`);
    const meal = await response.json();
    console.log(meal);
  } catch (error) {
    console.error('Error fetching meal details:', error);
  }
};

// Search meals
const searchMeals = async (searchTerm) => {
  try {
    const response = await fetch(`http://localhost:8082/api/meals/search?name=${searchTerm}`);
    const meals = await response.json();
    console.log(meals);
  } catch (error) {
    console.error('Error searching meals:', error);
  }
};

// Create new meal
const createMeal = async (mealData) => {
  try {
    const response = await fetch('http://localhost:8082/api/meals', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(mealData),
    });
    const newMeal = await response.json();
    console.log(newMeal);
  } catch (error) {
    console.error('Error creating meal:', error);
  }
};
```

---

## 📝 Notes

1. **CORS**: CORS is enabled for all origins (`*`). The frontend can call these APIs from any domain.

2. **Data Source**: 
   - Meals with `isExternal: true` are from TheMealDB API
   - Meals with `isExternal: false` are user-created

3. **Auto-Creation**: When creating a new meal, if category/area/ingredient doesn't exist, it will be automatically created.

4. **Database**: The API uses MySQL database with 595+ meals pre-loaded from TheMealDB.

5. **Authentication**: Currently, all endpoints are public (no authentication required). User authentication is being handled by another team member.

---

## 🐛 Troubleshooting

**Issue**: Cannot connect to API
- **Solution**: Make sure the backend server is running on port 8082

**Issue**: Getting 404 errors
- **Solution**: Check that you're using the correct endpoint paths (listed above)

**Issue**: POST request failing with 400
- **Solution**: Ensure all required fields are provided and properly formatted

**Issue**: Empty response
- **Solution**: Check if the database has data. The import runs automatically on first startup.

---

## 📧 Contact

For any questions or issues, please contact the backend team.

**Backend Repository**: `c:\Users\Lenovo\Full Stack Projects\Meal-Project\backend`
