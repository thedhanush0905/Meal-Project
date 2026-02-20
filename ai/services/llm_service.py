import os
import google.generativeai as genai
from typing import Optional


class LLMService:
    """Service to interact with Google Gemini LLM"""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gemini-2.5-flash"):
        """
        Initialize LLM Service for Google Gemini
        
        Args:
            api_key: Google Gemini API key (from environment or parameter)
            model: Model to use (default: gemini-pro)
        """
        # Get API key from parameter or environment
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        
        if not self.api_key:
            raise ValueError(
                "GEMINI_API_KEY not found. Please set it as environment variable or pass it directly."
            )
        
        # Initialize Gemini
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(model)
        self.model_name = model
        self.max_tokens = 500
        self.temperature = 0.7
    
    def generate_answer(self, prompt: str, temperature: Optional[float] = None, max_tokens: Optional[int] = None) -> str:
        """
        Generate answer using Google Gemini LLM
        
        Args:
            prompt: Input prompt for the model
            temperature: Sampling temperature (0-2)
            max_tokens: Maximum tokens in response
            
        Returns:
            Generated answer
        """
        try:
            temp = temperature if temperature is not None else self.temperature
            tokens = max_tokens if max_tokens is not None else self.max_tokens
            
            # Create system instruction
            system_instruction = "You are a helpful meal recommendation assistant with expertise in cooking, nutrition, and dietary preferences. Provide accurate, concise, and helpful advice."
            
            # Create generation config
            generation_config = genai.types.GenerationConfig(
                temperature=temp,
                max_output_tokens=tokens,
            )
            
            # Send request to Gemini
            response = self.model.generate_content(
                f"{system_instruction}\n\n{prompt}",
                generation_config=generation_config,
                stream=False
            )
            
            return response.text
        except Exception as e:
            error_msg = str(e)
            print(f"Error calling Gemini API with model '{self.model_name}': {error_msg}")
            raise Exception(f"Failed to generate answer with Gemini: {error_msg}")
    
    def generate_meal_suggestion(self, user_preferences: str) -> str:
        """
        Generate meal suggestions based on user preferences
        
        Args:
            user_preferences: Description of user's preferences
            
        Returns:
            Meal suggestion
        """
        prompt = f"""Based on the following preferences, suggest a meal and provide a brief recipe outline:
        
Preferences: {user_preferences}

Provide a meal name, key ingredients, and 3-4 quick preparation steps."""
        
        return self.generate_answer(prompt, max_tokens=300)
    
    def validate_meal_data(self, meal_name: str, ingredients: list, instructions: str) -> dict:
        """
        Use LLM to validate and enhance meal data
        
        Args:
            meal_name: Name of meal
            ingredients: List of ingredients
            instructions: Cooking instructions
            
        Returns:
            Validation result with suggestions
        """
        prompt = f"""Validate the following meal data and provide feedback:

Meal: {meal_name}
Ingredients: {', '.join(ingredients)}
Instructions: {instructions}

Provide:
1. Is this a valid meal? (Yes/No)
2. Any missing key ingredients?
3. Any issues with instructions?
4. Cuisine type suggestion"""
        
        answer = self.generate_answer(prompt, max_tokens=250)
        return {
            "meal_name": meal_name,
            "validation": answer
        }
