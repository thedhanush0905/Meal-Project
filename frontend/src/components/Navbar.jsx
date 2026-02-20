import { useState, useRef, useEffect } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { Home, List, PlusCircle, UtensilsCrossed, Bot, User, LogOut, ChevronDown } from 'lucide-react';

export default function Navbar() {
  const location = useLocation();
  const navigate = useNavigate();
  const [isProfileOpen, setIsProfileOpen] = useState(false);
  const dropdownRef = useRef(null);

  const navLinks = [
    { name: 'Home', path: '/home', icon: <Home className="w-5 h-5 mr-1" /> },
    { name: 'All Meals', path: '/meals', icon: <List className="w-5 h-5 mr-1" /> },
    { name: 'Add Meal', path: '/add-meal', icon: <PlusCircle className="w-5 h-5 mr-1" /> },
    { name: 'AI Query', path: '/ai-query', icon: <Bot className="w-5 h-5 mr-1" /> },
  ];

  // Close dropdown on outside click
  useEffect(() => {
    function handleClickOutside(event) {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setIsProfileOpen(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, [dropdownRef]);

  const handleLogout = () => {
    // Implement actual logout logic here (e.g., clear localStorage)
    setIsProfileOpen(false);
    navigate('/home'); 
  };

  return (
    <nav className="bg-white border-b border-gray-100 shadow-sm sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          
          {/* Logo Section */}
          <div className="flex items-center">
            <Link to="/home" className="flex items-center text-orange-500 hover:text-orange-600 transition-colors">
              <UtensilsCrossed className="w-8 h-8 mr-2" />
              <span className="font-bold text-2xl tracking-tight text-gray-900">
                Meal<span className="text-orange-500">Finder</span>
              </span>
            </Link>
          </div>

          {/* Center Nav Links */}
          <div className="hidden md:flex items-center space-x-2 lg:space-x-6">
            {navLinks.map((link) => {
              const isActive = location.pathname === link.path || (link.path !== '/' && link.path !== '/home' && location.pathname.startsWith(link.path));
              return (
                <Link
                  key={link.name}
                  to={link.path}
                  className={`flex items-center px-3 py-2 rounded-md text-sm font-medium transition-all duration-200 ${
                    isActive
                      ? 'text-orange-600 bg-orange-50'
                      : 'text-gray-600 hover:text-orange-500 hover:bg-gray-50'
                  }`}
                >
                  {link.icon}
                  {link.name}
                </Link>
              );
            })}
          </div>

          {/* Right Side - Profile Dropdown */}
          <div className="hidden md:relative md:flex items-center" ref={dropdownRef}>
            <button
              onClick={() => setIsProfileOpen(!isProfileOpen)}
              className="flex items-center gap-2 px-2 py-1.5 rounded-full hover:bg-gray-50 transition-colors focus:outline-none"
            >
              <div className="w-9 h-9 bg-gradient-to-br from-orange-400 to-orange-600 rounded-full flex items-center justify-center text-white shadow-sm">
                <User className="w-5 h-5" />
              </div>
              <ChevronDown className={`w-4 h-4 text-gray-500 transition-transform ${isProfileOpen ? 'rotate-180' : ''}`} />
            </button>

            {/* Dropdown Menu */}
            {isProfileOpen && (
              <div className="absolute right-0 top-full mt-2 w-48 bg-white rounded-xl shadow-lg border border-gray-100 py-1 origin-top overflow-hidden animate-fade-in">
                <Link 
                  to="/profile" 
                  onClick={() => setIsProfileOpen(false)}
                  className="flex items-center px-4 py-3 text-sm text-gray-700 hover:bg-orange-50 hover:text-orange-600 transition-colors"
                >
                  <User className="w-4 h-4 mr-3" /> Profile
                </Link>
                <div className="border-t border-gray-100"></div>
                <button 
                  onClick={handleLogout}
                  className="flex items-center w-full text-left px-4 py-3 text-sm text-red-600 hover:bg-red-50 transition-colors"
                >
                  <LogOut className="w-4 h-4 mr-3" /> Logout
                </button>
              </div>
            )}
          </div>
          
          {/* Mobile menu button (Simplified for now) */}
          <div className="flex items-center md:hidden">
             <div className="w-8 h-8 bg-orange-500 rounded-full flex items-center justify-center text-white">
                <User className="w-4 h-4" />
             </div>
          </div>
        </div>
      </div>
    </nav>
  );
}
