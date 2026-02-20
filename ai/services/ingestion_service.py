import chromadb
from typing import List, Dict, Any
from datetime import datetime
from .embedding_service import EmbeddingService
from models.schemas import MealData
import uuid


class IngestionService:
    """Service to ingest meals into ChromaDB"""
    
    def __init__(self, chroma_db_path: str = "./chroma_db"):
        """
        Initialize ingestion service
        
        Args:
            chroma_db_path: Path to ChromaDB storage
        """
        self.client = chromadb.PersistentClient(path=chroma_db_path)
        self.embedding_service = EmbeddingService()
    
    def ingest_meals(self, meals: List[MealData], collection_name: str = "meals") -> Dict[str, Any]:
        """
        Ingest meals into ChromaDB collection
        
        Args:
            meals: List of meal data to ingest
            collection_name: Name of collection to store meals
            
        Returns:
            Ingestion result with count and IDs
        """
        try:
            collection = self.client.get_or_create_collection(
                name=collection_name,
                metadata={"hnsw:space": "cosine"}
            )
            
            meal_ids = []
            documents = []
            embeddings = []
            metadatas = []
            
            for meal in meals:
                meal_id = meal.id or str(uuid.uuid4())
                meal_ids.append(meal_id)
                
                # Create searchable document
                doc = self.embedding_service.create_meal_document(meal.dict())
                documents.append(doc)
                
                # Generate embedding
                embedding = self.embedding_service.embed_text(doc)
                embeddings.append(embedding)
                
                # Store metadata
                metadata = meal.dict()
                metadata['ingested_at'] = datetime.now().isoformat()
                metadatas.append(metadata)
            
            # Add to collection
            collection.upsert(
                ids=meal_ids,
                documents=documents,
                embeddings=embeddings,
                metadatas=metadatas
            )
            
            return {
                "success": True,
                "meal_count": len(meals),
                "meal_ids": meal_ids,
                "collection": collection_name
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_collection_stats(self, collection_name: str = "meals") -> Dict[str, Any]:
        """
        Get statistics about a collection
        
        Args:
            collection_name: Name of collection
            
        Returns:
            Collection statistics
        """
        try:
            collection = self.client.get_collection(name=collection_name)
            count = collection.count()
            return {
                "success": True,
                "collection": collection_name,
                "meal_count": count
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
