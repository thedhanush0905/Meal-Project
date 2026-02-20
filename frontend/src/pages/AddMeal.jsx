import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Plus, Minus, Save, Loader2, Utensils } from 'lucide-react';
import { createMeal } from '../services/api';

export default function AddMeal() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  
  const [formData, setFormData] = useState({
    name: '',
    category: '',
    area: '',
    instructions: '',
    imageUrl: '',
    ingredients: [{ name: '', measure: '' }],
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleIngredientChange = (index, field, value) => {
    const newIngredients = [...formData.ingredients];
    newIngredients[index][field] = value;
    setFormData(prev => ({ ...prev, ingredients: newIngredients }));
  };

  const addIngredient = () => {
    setFormData(prev => ({
      ...prev,
      ingredients: [...prev.ingredients, { name: '', measure: '' }]
    }));
  };

  const removeIngredient = (index) => {
    if (formData.ingredients.length > 1) {
      const newIngredients = [...formData.ingredients];
      newIngredients.splice(index, 1);
      setFormData(prev => ({ ...prev, ingredients: newIngredients }));
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      // Basic validation
      if (!formData.name || !formData.instructions) {
        throw new Error('Name and instructions are required.');
      }

      await createMeal(formData);
      navigate('/meals');
    } catch (err) {
      console.error(err);
      setError(err.message || 'Failed to add meal. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto pb-20">
      
      <div className="bg-gradient-to-r from-orange-500 to-orange-600 rounded-[2.5rem] p-8 sm:p-12 text-white shadow-xl mb-12 flex items-center justify-between">
         <div>
           <h1 className="text-4xl font-extrabold tracking-tight mb-2">Create New Meal</h1>
           <p className="text-orange-100 text-lg">Share your delicious recipe with the community.</p>
         </div>
         <div className="hidden sm:flex bg-white/20 p-4 rounded-full">
            <Utensils className="w-12 h-12 text-white" />
         </div>
      </div>

      <form onSubmit={handleSubmit} className="bg-white rounded-[2rem] p-8 sm:p-10 shadow-sm border border-gray-100">
        
        {error && (
          <div className="mb-8 p-4 bg-red-50 text-red-600 rounded-xl font-medium border border-red-100">
            {error}
          </div>
        )}

        <div className="space-y-8">
          
          {/* Basic Info */}
          <section className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="col-span-1 md:col-span-2">
              <label className="block text-sm font-bold text-gray-700 mb-2">Meal Name *</label>
              <input 
                type="text" 
                name="name"
                value={formData.name}
                onChange={handleChange}
                className="w-full px-5 py-4 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-all outline-none"
                placeholder="e.g. Spicy Arrabiata Penne"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-bold text-gray-700 mb-2">Category</label>
              <input 
                type="text" 
                name="category"
                value={formData.category}
                onChange={handleChange}
                className="w-full px-5 py-4 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-all outline-none"
                placeholder="e.g. Pasta"
              />
            </div>

            <div>
              <label className="block text-sm font-bold text-gray-700 mb-2">Area / Cuisine</label>
              <input 
                type="text" 
                name="area"
                value={formData.area}
                onChange={handleChange}
                className="w-full px-5 py-4 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-all outline-none"
                placeholder="e.g. Italian"
              />
            </div>

            <div className="col-span-1 md:col-span-2">
              <label className="block text-sm font-bold text-gray-700 mb-2">Image URL</label>
              <input 
                type="url" 
                name="imageUrl"
                value={formData.imageUrl}
                onChange={handleChange}
                className="w-full px-5 py-4 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-all outline-none"
                placeholder="https://example.com/image.jpg"
              />
            </div>
          </section>

          <hr className="border-gray-100 my-8" />

          {/* Ingredients Section */}
          <section>
            <div className="flex justify-between items-center mb-6">
              <h3 className="text-xl font-bold text-gray-900">Ingredients</h3>
              <button 
                type="button" 
                onClick={addIngredient}
                className="flex items-center text-sm font-bold text-orange-600 hover:text-orange-700 bg-orange-50 px-4 py-2 rounded-lg transition-colors"
              >
                <Plus className="w-4 h-4 mr-1" /> Add Item
              </button>
            </div>

            <div className="space-y-4">
              {formData.ingredients.map((ingredient, idx) => (
                <div key={idx} className="flex items-center gap-4">
                  <div className="flex-1">
                    <input 
                      type="text" 
                      placeholder="Ingredient Name (e.g. Garlic)"
                      value={ingredient.name}
                      onChange={(e) => handleIngredientChange(idx, 'name', e.target.value)}
                      className="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-orange-500 focus:border-transparent outline-none"
                      required
                    />
                  </div>
                  <div className="flex-1">
                    <input 
                      type="text" 
                      placeholder="Measure (e.g. 2 cloves)"
                      value={ingredient.measure}
                      onChange={(e) => handleIngredientChange(idx, 'measure', e.target.value)}
                      className="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-orange-500 focus:border-transparent outline-none"
                      required
                    />
                  </div>
                  {formData.ingredients.length > 1 && (
                    <button 
                      type="button" 
                      onClick={() => removeIngredient(idx)}
                      className="p-3 text-red-500 hover:bg-red-50 rounded-xl transition-colors"
                    >
                      <Minus className="w-5 h-5" />
                    </button>
                  )}
                </div>
              ))}
            </div>
          </section>

          <hr className="border-gray-100 my-8" />

          {/* Instructions Option */}
          <section>
             <label className="block text-sm font-bold text-gray-700 mb-2">Instructions *</label>
             <textarea 
               name="instructions"
               value={formData.instructions}
               onChange={handleChange}
               rows="6"
               className="w-full px-5 py-4 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-all outline-none resize-y"
               placeholder="Write down the step-by-step instructions..."
               required
             ></textarea>
          </section>

        </div>

        <div className="mt-10 pt-8 border-t border-gray-100 flex justify-end">
          <button 
            type="submit" 
            disabled={loading}
            className="flex items-center justify-center px-10 py-4 bg-gray-900 text-white font-bold rounded-xl shadow-lg shadow-gray-900/20 hover:bg-gray-800 hover:shadow-xl transition-all disabled:opacity-70 disabled:cursor-not-allowed min-w-[200px]"
          >
            {loading ? (
              <Loader2 className="w-6 h-6 animate-spin" />
            ) : (
              <><Save className="w-5 h-5 mr-2" /> Save Meal</>
            )}
          </button>
        </div>
      </form>
    </div>
  );
}
