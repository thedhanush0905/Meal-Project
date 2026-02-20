from typing import List, Dict, Any
from .ingestion_service import IngestionService
from .rag_service import RAGService
from .decision_router import DecisionRouter
from models.schemas import MealData, RAGResponse


class MealAIService:
    """Main service orchestrating AI operations for meals"""
    
    def __init__(self, chroma_db_path: str = "./chroma_db"):
        """
        Initialize Meal AI Service
        
        Args:
            chroma_db_path: Path to ChromaDB storage
        """
        self.ingestion_service = IngestionService(chroma_db_path)
        self.rag_service = RAGService(chroma_db_path)
        self.decision_router = DecisionRouter()
    
    def add_user_meal(self, meal: MealData, collection_name: str = "meals") -> Dict[str, Any]:
        """
        Add a new user meal to ChromaDB
        
        Args:
            meal: Meal data to add
            collection_name: Collection name
            
        Returns:
            Result of ingestion
        """
        result = self.ingestion_service.ingest_meals([meal], collection_name)
        return result
    
    def add_meals_batch(self, meals: List[MealData], collection_name: str = "meals") -> Dict[str, Any]:
        """
        Add multiple meals to ChromaDB
        
        Args:
            meals: List of meals to add
            collection_name: Collection name
            
        Returns:
            Result of ingestion
        """
        result = self.ingestion_service.ingest_meals(meals, collection_name)
        return result
    
    def answer_meal_query(self, query: str, top_k: int = 5, collection_name: str = "meals") -> RAGResponse:
        """
        Answer query about meals using RAG
        
        Args:
            query: User query
            top_k: Number of meals to retrieve
            collection_name: Collection name
            
        Returns:
            RAG response with answer and retrieved meals
        """
        return self.rag_service.answer_query(query, top_k, collection_name)
    
    def get_collection_status(self, collection_name: str = "meals") -> Dict[str, Any]:
        """
        Get status of a collection
        
        Args:
            collection_name: Collection name
            
        Returns:
            Collection statistics
        """
        return self.ingestion_service.get_collection_stats(collection_name)
