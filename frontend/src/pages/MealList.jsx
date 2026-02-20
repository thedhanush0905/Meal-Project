import { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { Search, Loader2, Utensils } from 'lucide-react';
import MealCard from '../components/MealCard';
import { getMeals, searchMeals } from '../services/api';

export default function MealList() {
  const [meals, setMeals] = useState([]);
  const [loading, setLoading] = useState(true);
  const location = useLocation();
  const navigate = useNavigate();
  
  // Extract search query from URL
  const queryParams = new URLSearchParams(location.search);
  const initialSearch = queryParams.get('search') || '';
  const [searchInput, setSearchInput] = useState(initialSearch);

  useEffect(() => {
    const fetchMeals = async () => {
      setLoading(true);
      try {
        let response;
        if (initialSearch) {
          response = await searchMeals(initialSearch);
        } else {
          response = await getMeals();
        }
        
        // Handle variations in API response structure safely
        if (response.data) {
          // If the API returns `{ meals: [...] }` or just `[...]`
          const mealData = response.data.meals || response.data;
          setMeals(Array.isArray(mealData) ? mealData : []);
        } else {
          setMeals([]);
        }
      } catch (error) {
        console.error("Error fetching meals:", error);
        setMeals([]);
      } finally {
        setLoading(false);
      }
    };

    fetchMeals();
  }, [initialSearch]);

  const handleSearch = (e) => {
    e.preventDefault();
    if (searchInput.trim()) {
      navigate(`/meals?search=${encodeURIComponent(searchInput)}`);
    } else {
      navigate(`/meals`);
    }
  };

  return (
    <div className="flex flex-col gap-10">
      
      {/* Header & Search */}
      <div className="bg-white rounded-3xl p-8 shadow-sm border border-gray-100 flex flex-col md:flex-row items-center justify-between gap-6">
        <div>
           <h1 className="text-3xl font-bold text-gray-900 mb-2">
             {initialSearch ? `Search Results for "${initialSearch}"` : "All Delicious Meals"}
           </h1>
           <p className="text-gray-500">
             {initialSearch 
               ? `Found ${meals.length} recipes matching your crave.` 
               : "Browse through our extensive collection of recipes."}
           </p>
        </div>

        <form onSubmit={handleSearch} className="w-full md:w-96 relative group">
           <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
             <Search className="h-5 w-5 text-gray-400 group-focus-within:text-blue-600 transition-colors" />
           </div>
           <input
             type="text"
             className="block w-full pl-11 pr-4 py-3 rounded-full text-gray-900 bg-gray-50 border border-gray-200 focus:ring-2 focus:ring-blue-500 focus:border-transparent focus:outline-none transition-all"
             placeholder="Re-search meals..."
             value={searchInput}
             onChange={(e) => setSearchInput(e.target.value)}
           />
        </form>
      </div>

      {/* Grid */}
      {loading ? (
        <div className="flex flex-col items-center justify-center py-20">
          <Loader2 className="w-12 h-12 text-blue-600 animate-spin mb-4" />
          <p className="text-gray-500 font-medium">Cooking up the results...</p>
        </div>
      ) : meals.length > 0 ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-8">
          {meals.map(meal => (
            <MealCard key={meal.idMeal || meal.id} meal={meal} />
          ))}
        </div>
      ) : (
        <div className="flex flex-col items-center justify-center py-24 bg-white rounded-3xl border border-dashed border-gray-300 text-center px-4">
          <div className="bg-orange-100 p-4 rounded-full mb-4">
             <Utensils className="w-8 h-8 text-orange-600" />
          </div>
          <h3 className="text-xl font-bold text-gray-900 mb-2">No meals found</h3>
          <p className="text-gray-500 max-w-md">
            We couldn't find any meals matching your search. Try different keywords or browse all meals.
          </p>
          {initialSearch && (
            <button 
              onClick={() => navigate('/meals')}
              className="mt-6 px-6 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-full font-medium transition-colors"
            >
              Clear Search
            </button>
          )}
        </div>
      )}

    </div>
  );
}
