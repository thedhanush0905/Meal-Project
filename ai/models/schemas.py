from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class MealData(BaseModel):
    """Schema for a meal item"""
    id: Optional[str] = None
    name: str
    description: str
    ingredients: List[str]
    instructions: str
    calories: Optional[int] = None
    cuisine: Optional[str] = None
    dietary_tags: Optional[List[str]] = None
    source: str = "user_added"  # Can be 'mealdb', 'user_added', etc.
    created_at: Optional[datetime] = None


class IngestionRequest(BaseModel):
    """Schema for ingesting a new meal into ChromaDB"""
    meals: List[MealData]
    collection_name: str = "meals"


class QueryRequest(BaseModel):
    """Schema for RAG query request"""
    prompt: str
    top_k: int = 5
    collection_name: str = "meals"


class MealRetrievalResult(BaseModel):
    """Schema for meal retrieval results"""
    meal_name: str
    description: str
    relevance_score: float
    source: str


class RAGResponse(BaseModel):
    """Schema for RAG response"""
    answer: str
    retrieved_meals: List[MealRetrievalResult]
    confidence: float
