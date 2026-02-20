import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getMealById, getMealCalories } from '../services/api';
import { ArrowLeft, Flame, Globe, LayoutList, Loader2, Utensils } from 'lucide-react';

export default function MealDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [meal, setMeal] = useState(null);
  const [nutrition, setNutrition] = useState(null);
  const [loading, setLoading] = useState(true);
  const [nutritionLoading, setNutritionLoading] = useState(false);

  useEffect(() => {
    const fetchMealData = async () => {
      setLoading(true);
      try {
        const res = await getMealById(id);
        const mealData = res.data?.meals ? res.data.meals[0] : res.data;
        setMeal(mealData);

        // Fetch calories data in parallel or right after
        if (mealData) {
          fetchNutrition(id);
        }
      } catch (err) {
        console.error("Failed to load meal details", err);
      } finally {
        setLoading(false);
      }
    };

    fetchMealData();
  }, [id]);

  const fetchNutrition = async (mealId) => {
    setNutritionLoading(true);
    try {
      const res = await getMealCalories(mealId);
      setNutrition(res.data);
    } catch (err) {
      console.error("Failed to fetch nutrition data", err);
    } finally {
      setNutritionLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center py-32">
        <Loader2 className="w-12 h-12 text-blue-600 animate-spin" />
      </div>
    );
  }

  if (!meal) {
    return (
      <div className="text-center py-20 bg-white rounded-3xl border border-gray-100 shadow-sm mt-8">
        <h2 className="text-2xl font-bold text-gray-900">Meal Not Found</h2>
        <button onClick={() => navigate('/meals')} className="mt-4 text-blue-600 font-medium hover:underline">
          Return to All Meals
        </button>
      </div>
    );
  }

  // Extract ingredients from the MealDB format (strIngredient1..20 and strMeasure1..20)
  // If the backend has already normalized it, we can use the nutrition API data. We will rely on nutrition API data if available.
  const getIngredientsList = () => {
    const list = [];
    for (let i = 1; i <= 20; i++) {
      const ingredient = meal[`strIngredient${i}`];
      const measure = meal[`strMeasure${i}`];
      if (ingredient && ingredient.trim() !== "") {
        list.push({ name: ingredient, measure: measure || "" });
      }
    }
    return list;
  };
  
  const rawIngredients = getIngredientsList();
  const displayIngredients = nutrition?.ingredients || rawIngredients;

  return (
    <div className="animate-fade-in max-w-5xl mx-auto pb-16">
      <button 
        onClick={() => navigate(-1)} 
        className="group flex items-center text-gray-500 hover:text-gray-900 mb-8 font-medium transition-colors"
      >
        <ArrowLeft className="w-5 h-5 mr-2 group-hover:-translate-x-1 transition-transform" /> Back
      </button>

      {/* Header Section */}
      <div className="bg-white rounded-[2.5rem] p-4 shadow-xl border border-gray-100 mb-12 flex flex-col md:flex-row gap-8 items-center overflow-hidden">
        <div className="w-full md:w-1/2 aspect-square md:aspect-[4/3] rounded-[2rem] overflow-hidden shadow-inner flex-shrink-0">
          <img 
            src={meal.strMealThumb || meal.imageUrl} 
            alt={meal.strMeal || meal.name}
            className="w-full h-full object-cover hover:scale-105 transition-transform duration-700" 
          />
        </div>
        <div className="w-full md:w-1/2 p-4 md:p-8 flex flex-col justify-center">
          <div className="flex gap-3 mb-4">
             {meal.strCategory && (
               <span className="flex items-center text-sm font-bold bg-orange-100 text-orange-700 px-3 py-1 rounded-full">
                 <LayoutList className="w-4 h-4 mr-1" /> {meal.strCategory}
               </span>
             )}
             {meal.strArea && (
               <span className="flex items-center text-sm font-bold bg-blue-100 text-blue-700 px-3 py-1 rounded-full">
                 <Globe className="w-4 h-4 mr-1" /> {meal.strArea}
               </span>
             )}
          </div>
          <h1 className="text-4xl sm:text-5xl font-extrabold text-gray-900 mb-6 tracking-tight">
            {meal.strMeal || meal.name}
          </h1>

          {/* Calorie Card Mini */}
          <div className="bg-gradient-to-br from-gray-900 to-gray-800 rounded-3xl p-6 text-white shadow-lg mt-4 max-w-sm">
            <div className="flex justify-between items-center mb-2">
              <span className="text-gray-400 font-medium flex items-center"><Flame className="w-5 h-5 mr-1 text-orange-500"/> Total Calories</span>
              {nutritionLoading && <Loader2 className="w-5 h-5 animate-spin text-gray-400" />}
            </div>
            <div className="text-4xl font-black text-transparent bg-clip-text bg-gradient-to-r from-orange-400 to-yellow-400">
               {nutrition ? `${nutrition.totalCalories} kcal` : '...'}
            </div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-12">
        
        {/* Left Column: Ingredients */}
        <div className="lg:col-span-1 space-y-8">
          <section className="bg-white rounded-3xl p-8 shadow-sm border border-gray-100">
            <h2 className="text-2xl font-bold text-gray-900 mb-6 flex items-center">
              <Utensils className="w-6 h-6 mr-2 text-orange-500" /> Ingredients
            </h2>
            
            <ul className="space-y-4">
              {displayIngredients.map((ing, idx) => (
                <li key={idx} className="flex justify-between items-center py-2 border-b border-gray-50 last:border-0">
                  <span className="font-semibold text-gray-800 capitalize">{ing.name}</span>
                  <div className="text-right">
                     <span className="text-sm text-gray-500 block">{ing.measure}</span>
                     {ing.calories !== undefined && (
                        <span className="text-xs font-bold text-orange-500">{ing.calories} kcal</span>
                     )}
                  </div>
                </li>
              ))}
            </ul>
          </section>
        </div>

        {/* Right Column: Instructions */}
        <div className="lg:col-span-2 space-y-8">
          <section className="bg-white rounded-3xl p-8 lg:p-12 shadow-sm border border-gray-100">
            <h2 className="text-3xl font-bold text-gray-900 mb-8">Instructions</h2>
            <div className="prose prose-lg max-w-none text-gray-600">
               {(meal.strInstructions || meal.instructions || "No instructions provided.").split('\n').filter(p => p.trim() !== '').map((paragraph, idx) => (
                 <p key={idx} className="mb-4 leading-relaxed bg-gray-50 p-4 rounded-2xl border border-gray-100">
                   {paragraph}
                 </p>
               ))}
            </div>

            {meal.strYoutube && (
              <div className="mt-12 pt-8 border-t border-gray-100">
                <a 
                  href={meal.strYoutube} 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="inline-flex items-center justify-center px-8 py-4 bg-red-600 hover:bg-red-700 text-white font-bold rounded-xl shadow-lg shadow-red-600/30 transition-all"
                >
                  Watch Video Tutorial
                </a>
              </div>
            )}
          </section>
        </div>
      

      </div>
    </div>
  );
}
