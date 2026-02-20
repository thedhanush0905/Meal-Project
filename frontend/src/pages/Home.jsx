import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Search, ArrowRight, Sparkles, ChefHat } from 'lucide-react';
import MealCard from '../components/MealCard';
import { getMeals, searchMeals, getLeastIngredientsMeal } from '../services/api';

export default function Home() {
  const [searchQuery, setSearchQuery] = useState('');
  const [featuredMeal, setFeaturedMeal] = useState(null);
  const [popularMeals, setPopularMeals] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchInitialData = async () => {
      try {
        setLoading(true);
        // Try to fetch least ingredients meal
        try {
          const featuredRes = await getLeastIngredientsMeal();
          if (featuredRes.data) setFeaturedMeal(featuredRes.data);
        } catch (err) {
          console.error("Failed to fetch featured meal", err);
        }

        // Fetch some meals for popular section
        const mealsRes = await getMeals();
        if (mealsRes.data && mealsRes.data.length > 0) {
          // Take first 6 meals for the landing page
          setPopularMeals(mealsRes.data.slice(0, 6));
        }
      } catch (error) {
        console.error("Error fetching landing page data:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchInitialData();
  }, []);

  const handleSearch = async (e) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      // Navigate to meal list with search query in state or URL
      // For simplicity, let's navigate to /meals and we can handle search there,
      // or we can handle search results right here. Let's just navigate.
      navigate(`/meals?search=${encodeURIComponent(searchQuery)}`);
    }
  };

  return (
    <div className="flex flex-col gap-16 pb-16">
      
      {/* Hero Section */}
      <section className="relative rounded-3xl bg-gradient-to-br from-orange-400 to-orange-600 overflow-hidden shadow-2xl mt-4">
        {/* Abstract Background pattern */}
        <div className="absolute inset-0 opacity-10 bg-[radial-gradient(ellipse_at_center,_var(--tw-gradient-stops))] from-white via-transparent to-transparent"></div>
        
        <div className="relative px-6 py-16 sm:py-24 lg:px-12 text-center text-white flex flex-col items-center">
           <ChefHat className="w-16 h-16 mb-6 opacity-90" />
           <h1 className="text-4xl sm:text-5xl lg:text-6xl font-extrabold tracking-tight mb-6">
             Discover Your Next <br/> <span className="text-orange-200">Favorite Meal</span>
           </h1>
           <p className="max-w-2xl text-lg sm:text-xl text-orange-100 mb-10 font-medium">
             Search through thousands of recipes, calculate precise calories, and get AI-powered nutrition suggestions.
           </p>

           <form onSubmit={handleSearch} className="w-full max-w-xl mx-auto relative group">
              <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                <Search className="h-6 w-6 text-gray-400 group-focus-within:text-orange-500 transition-colors" />
              </div>
              <input
                type="text"
                className="block w-full pl-12 pr-4 py-4 rounded-full text-gray-900 bg-white shadow-xl focus:ring-4 focus:ring-orange-300 focus:outline-none text-lg transition-all"
                placeholder="Search for 'Arrabiata' or 'Chicken'..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
              />
              <button 
                type="submit"
                className="absolute right-2 top-2 bottom-2 px-6 bg-gray-900 text-white rounded-full font-semibold hover:bg-gray-800 transition-colors flex items-center shadow-md shadow-gray-900/20"
              >
                Search
              </button>
           </form>
        </div>
      </section>

      {/* Featured Meal Section */}
      {!loading && featuredMeal && (
        <section className="max-w-5xl mx-auto w-full">
          <div className="flex items-center gap-2 mb-6">
            <Sparkles className="w-6 h-6 text-yellow-500" />
            <h2 className="text-2xl font-bold text-gray-900">Featured: Least Ingredients</h2>
          </div>
          
          <div className="bg-white rounded-[2rem] p-6 sm:p-8 flex flex-col md:flex-row gap-8 shadow-xl shadow-orange-100/50 border border-orange-50 items-center">
             <div className="w-full md:w-1/2 aspect-video md:aspect-square max-h-[400px] overflow-hidden rounded-2xl shadow-inner">
               <img 
                 src={featuredMeal.strMealThumb || featuredMeal.imageUrl} 
                 alt={featuredMeal.strMeal || featuredMeal.name}
                 className="w-full h-full object-cover hover:scale-105 transition-transform duration-700" 
               />
             </div>
             
             <div className="w-full md:w-1/2 flex flex-col justify-center">
               <div className="inline-block px-4 py-1.5 bg-green-100 text-green-700 rounded-full text-sm font-bold w-max mb-4">
                 Easiest to Cook
               </div>
               <h3 className="text-3xl font-extrabold text-gray-900 mb-4">{featuredMeal.strMeal || featuredMeal.name}</h3>
               <p className="text-gray-600 text-lg mb-8 leading-relaxed">
                 Looking for a quick meal without a massive grocery list? This meal minimizes the ingredients without sacrificing flavor.
               </p>
               <button 
                 onClick={() => navigate(`/meals/${featuredMeal.idMeal || featuredMeal.id}`)}
                 className="flex items-center gap-2 w-max px-8 py-4 bg-orange-600 hover:bg-orange-700 text-white rounded-xl font-bold text-lg shadow-lg shadow-orange-600/30 transition-all hover:pr-6 hover:pl-10"
               >
                 View Recipe <ArrowRight className="w-5 h-5" />
               </button>
             </div>
          </div>
        </section>
      )}

      {/* Popular Meals Section */}
      <section>
        <div className="flex items-center justify-between mb-8">
          <h2 className="text-2xl font-bold text-gray-900 tracking-tight">Trending Meals</h2>
          <button 
            onClick={() => navigate('/meals')}
            className="text-orange-600 font-semibold hover:text-orange-700 flex items-center gap-1 group"
          >
            View All <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
          </button>
        </div>
        
        {loading ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
            {[1, 2, 3].map(i => (
              <div key={i} className="animate-pulse bg-white rounded-2xl h-80 border border-gray-100">
                <div className="bg-gray-200 h-48 rounded-t-2xl"></div>
                <div className="p-5 space-y-4">
                  <div className="h-6 bg-gray-200 rounded w-3/4"></div>
                  <div className="h-4 bg-gray-200 rounded w-1/2"></div>
                </div>
              </div>
            ))}
          </div>
        ) : popularMeals.length > 0 ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
            {popularMeals.map(meal => (
              <MealCard key={meal.idMeal || meal.id} meal={meal} />
            ))}
          </div>
        ) : (
          <div className="text-center py-12 text-gray-500 bg-white rounded-2xl border border-dashed border-gray-300">
            No meals available to display right now.
          </div>
        )}
      </section>

    </div>
  );
}
