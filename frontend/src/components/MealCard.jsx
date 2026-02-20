import { Link } from 'react-router-dom';
import { Clock, Users } from 'lucide-react';

export default function MealCard({ meal }) {
  // Graceful fallback for missing data
  if (!meal) return null;

  return (
    <Link 
      to={`/meals/${meal.idMeal || meal.id}`} 
      className="group flex flex-col bg-white rounded-2xl overflow-hidden shadow-sm hover:shadow-xl hover:-translate-y-1 transition-all duration-300 border border-gray-100"
    >
      <div className="relative h-48 sm:h-56 overflow-hidden bg-gray-100">
        <img 
          src={meal.strMealThumb || meal.imageUrl || 'https://via.placeholder.com/400x300?text=No+Image'} 
          alt={meal.strMeal || meal.name} 
          className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
          loading="lazy"
        />
        {meal.strCategory && (
          <div className="absolute top-3 right-3 bg-white/90 backdrop-blur-sm px-3 py-1 rounded-full text-xs font-semibold text-orange-600 shadow-sm">
            {meal.strCategory}
          </div>
        )}
      </div>
      
      <div className="p-5 flex-1 flex flex-col">
        <h3 className="text-lg font-bold text-gray-900 mb-2 line-clamp-2 group-hover:text-orange-600 transition-colors">
          {meal.strMeal || meal.name}
        </h3>
        
        {meal.strArea && (
           <p className="text-sm text-gray-500 mb-4">{meal.strArea} Cuisine</p>
        )}

        <div className="mt-auto flex items-center justify-between text-sm text-gray-500 pt-4 border-t border-gray-50">
          <div className="flex items-center">
             <Clock className="w-4 h-4 mr-1" />
             <span>30 Min</span>
          </div>
          <div className="flex items-center text-orange-500 font-medium group-hover:underline">
             View Recipe
          </div>
        </div>
      </div>
    </Link>
  );
}
