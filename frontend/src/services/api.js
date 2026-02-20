const API_URL = 'http://localhost:8080/api';

export const queryAI = async (query) => {
  try {
    const response = await fetch(`${API_URL}/ai/query`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ query }),
    });

    if (!response.ok) {
      throw new Error('AI service failed to respond');
    }

    return await response.json();
  } catch (error) {
    console.error('API Error:', error);
    throw error;
  }
};

export const getLeastIngredientsMeal = async () => {
  // Fake "least ingredients" by getting a random meal
  const res = await api.get('/random.php');
  const meal = res.data.meals ? res.data.meals[0] : null;
  return { data: meal }; // Landing expects res.data to be the meal object directly
};

export const getMealCalories = async (id) => {
  // Mock artificial calorie response 
  await new Promise(resolve => setTimeout(resolve, 600));
  return {
    data: {
      totalCalories: Math.floor(Math.random() * 400) + 300,
      ingredients: [] // fallback to MealDB ingredients
    }
  };
};

export const createMeal = async (mealData) => {
  // Mock POST request 
  await new Promise(resolve => setTimeout(resolve, 1000));
  return { data: { message: "Meal saved successfully (Mocked)" } };
};

export default api;
