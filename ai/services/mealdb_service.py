import requests
from typing import List, Dict, Any
from models.schemas import MealData


class MealDBService:
    """Service to fetch meals from MealDB API (https://www.themealdb.com/api.php)"""
    
    BASE_URL = "https://www.themealdb.com/api/json/v1/1"
    
    def __init__(self):
        self.session = requests.Session()
    
    def search_meals_by_name(self, name: str) -> List[Dict[str, Any]]:
        """
        Search meals by name from MealDB
        
        Args:
            name: Meal name to search for
            
        Returns:
            List of meals matching the search
        """
        try:
            url = f"{self.BASE_URL}/search.php"
            params = {"s": name}
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            return data.get("meals", []) if data.get("meals") else []
        except Exception as e:
            print(f"Error searching meals by name '{name}': {str(e)}")
            return []
    
    def get_random_meals(self, count: int = 50) -> List[Dict[str, Any]]:
        """
        Fetch random meals from MealDB
        
        Args:
            count: Number of random meals to fetch
            
        Returns:
            List of random meals
        """
        meals = []
        for i in range(count):
            try:
                url = f"{self.BASE_URL}/random.php"
                response = self.session.get(url, timeout=10)
                response.raise_for_status()
                
                data = response.json()
                if data.get("meals"):
                    meals.append(data["meals"][0])
            except Exception as e:
                print(f"Error fetching random meal {i+1}: {str(e)}")
                continue
        
        return meals
    
    def get_meals_by_category(self, category: str) -> List[Dict[str, Any]]:
        """
        Get all meals in a category
        
        Args:
            category: Category name (e.g., 'Seafood', 'Vegetarian', 'Dessert')
            
        Returns:
            List of meals in category
        """
        try:
            url = f"{self.BASE_URL}/filter.php"
            params = {"c": category}
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            return data.get("meals", []) if data.get("meals") else []
        except Exception as e:
            print(f"Error fetching meals for category '{category}': {str(e)}")
            return []
    
    def convert_to_meal_data(self, mealdb_meal: Dict[str, Any]) -> MealData:
        """
        Convert MealDB meal format to our MealData schema
        
        Args:
            mealdb_meal: Meal data from MealDB API
            
        Returns:
            MealData object
        """
        # Extract ingredients and measurements
        ingredients = []
        for i in range(1, 21):  # MealDB has up to 20 ingredients
            ingredient_key = f"strIngredient{i}"
            measure_key = f"strMeasure{i}"
            
            ingredient = mealdb_meal.get(ingredient_key, "").strip()
            measure = mealdb_meal.get(measure_key, "").strip()
            
            if ingredient:
                ingredients.append(f"{measure} {ingredient}".strip() if measure else ingredient)
        
        # Create MealData object
        meal = MealData(
            id=mealdb_meal.get("idMeal"),
            name=mealdb_meal.get("strMeal", "Unknown"),
            description=f"{mealdb_meal.get('strArea', 'Unknown')} {mealdb_meal.get('strCategory', '')} meal",
            ingredients=ingredients if ingredients else ["No ingredients listed"],
            instructions=mealdb_meal.get("strInstructions", "No instructions provided"),
            cuisine=mealdb_meal.get("strArea", "Unknown"),
            dietary_tags=[mealdb_meal.get("strCategory", "")] if mealdb_meal.get("strCategory") else [],
            source="mealdb",
        )
        
        return meal
    
    def fetch_popular_meals(self) -> List[MealData]:
        """
        Fetch popular meals from common categories
        
        Returns:
            List of MealData objects
        """
        categories = ["Seafood", "Breakfast", "Dessert", "Vegetarian", "Pasta", "Chicken"]
        all_meals = []
        
        for category in categories:
            print(f"Fetching meals from category: {category}")
            meals_list = self.get_meals_by_category(category)
            
            # Limit to first 5 meals per category to avoid too many requests
            for meal_summary in meals_list[:5]:
                try:
                    # Get full meal details
                    meal_id = meal_summary.get("idMeal")
                    full_meal = self.get_meal_by_id(meal_id)
                    
                    if full_meal:
                        meal_data = self.convert_to_meal_data(full_meal)
                        all_meals.append(meal_data)
                except Exception as e:
                    print(f"Error processing meal: {str(e)}")
                    continue
        
        return all_meals
    
    def get_meal_by_id(self, meal_id: str) -> Dict[str, Any]:
        """
        Get full meal details by ID
        
        Args:
            meal_id: MealDB meal ID
            
        Returns:
            Full meal data
        """
        try:
            url = f"{self.BASE_URL}/lookup.php"
            params = {"i": meal_id}
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            if data.get("meals"):
                return data["meals"][0]
            return None
        except Exception as e:
            print(f"Error fetching meal {meal_id}: {str(e)}")
            return None
