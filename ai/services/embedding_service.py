from sentence_transformers import SentenceTransformer
from typing import List


class EmbeddingService:
    """Service to generate embeddings for meal data"""
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize embedding service
        
        Args:
            model_name: HuggingFace model for embeddings
        """
        self.model = SentenceTransformer(model_name)
    
    def embed_text(self, text: str) -> List[float]:
        """
        Convert text to embedding vector
        
        Args:
            text: Input text to embed
            
        Returns:
            Embedding vector
        """
        embedding = self.model.encode(text, convert_to_tensor=False)
        return embedding.tolist()
    
    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Convert multiple texts to embedding vectors
        
        Args:
            texts: List of texts to embed
            
        Returns:
            List of embedding vectors
        """
        embeddings = self.model.encode(texts, convert_to_tensor=False)
        return [emb.tolist() for emb in embeddings]
    
    def create_meal_document(self, meal_data: dict) -> str:
        """
        Create searchable document from meal data
        
        Args:
            meal_data: Dictionary with meal information
            
        Returns:
            Combined text for embedding
        """
        parts = [
            meal_data.get("name", ""),
            meal_data.get("description", ""),
            " ".join(meal_data.get("ingredients", [])),
            meal_data.get("cuisine", ""),
            " ".join(meal_data.get("dietary_tags", []))
        ]
        return " ".join([str(p) for p in parts if p])
