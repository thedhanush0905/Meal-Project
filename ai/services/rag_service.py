import chromadb
from typing import List, Dict, Any
from .embedding_service import EmbeddingService
from .llm_service import LLMService
from models.schemas import MealRetrievalResult, RAGResponse


class RAGService:
    """Service for Retrieval-Augmented Generation with meals"""
    
    def __init__(self, chroma_db_path: str = "./chroma_db"):
        """
        Initialize RAG service
        
        Args:
            chroma_db_path: Path to ChromaDB storage
        """
        self.client = chromadb.PersistentClient(path=chroma_db_path)
        self.embedding_service = EmbeddingService()
        self.llm_service = LLMService()
    
    def retrieve_relevant_meals(self, query: str, top_k: int = 5, collection_name: str = "meals") -> List[Dict[str, Any]]:
        """
        Retrieve meals relevant to query from ChromaDB with dietary constraint filtering
        
        Args:
            query: Search query
            top_k: Number of results to retrieve
            collection_name: Collection to search in
            
        Returns:
            List of relevant meals with metadata and relevance scores
        """
        try:
            collection = self.client.get_collection(name=collection_name)
            
            # Generate query embedding
            query_embedding = self.embedding_service.embed_text(query)
            
            # Query collection - get more results to allow filtering
            results = collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k * 3,  # Get 3x more to filter
                include=["documents", "metadatas", "distances"]
            )
            
            # Format results with filtering
            meals = []
            dietary_constraints = self._extract_dietary_constraints(query)
            
            if results and results['ids'] and len(results['ids']) > 0:
                for i, meal_id in enumerate(results['ids'][0]):
                    # Convert distance to similarity score (cosine distance)
                    distance = results['distances'][0][i]
                    similarity = 1 - distance  # Convert distance to similarity
                    
                    metadata = results['metadatas'][0][i]
                    meal_dietary_tags = metadata.get('dietary_tags', [])
                    meal_name = metadata.get('name', '').lower()
                    meal_ingredients = [ing.lower() for ing in metadata.get('ingredients', [])]
                    
                    # Check dietary constraint compatibility
                    if self._matches_dietary_constraints(query, dietary_constraints, meal_dietary_tags, meal_name, meal_ingredients, similarity):
                        meal = {
                            "id": meal_id,
                            "name": metadata.get('name', ''),
                            "description": metadata.get('description', ''),
                            "ingredients": metadata.get('ingredients', []),
                            "instructions": metadata.get('instructions', ''),
                            "source": metadata.get('source', ''),
                            "cuisine": metadata.get('cuisine', ''),
                            "dietary_tags": meal_dietary_tags,
                            "relevance_score": float(similarity)
                        }
                        meals.append(meal)
                        
                        # Stop when we have enough quality results
                        if len(meals) >= top_k:
                            break
            
            return meals[:top_k]
        except Exception as e:
            print(f"Error retrieving meals: {str(e)}")
            return []
    
    def _extract_dietary_constraints(self, query: str) -> Dict[str, bool]:
        """Extract dietary constraints from query"""
        query_lower = query.lower()
        return {
            "vegetarian": any(word in query_lower for word in ["veg", "vegetarian", "vegan", "tofu", "beans", "lentil", "no meat", "no chicken", "no fish"]),
            "non_veg": any(word in query_lower for word in ["chicken", "meat", "fish", "seafood", "beef", "pork", "lamb"]),
            "seafood": any(word in query_lower for word in ["fish", "seafood", "shrimp", "prawn", "salmon", "tuna"]),
            "chicken": any(word in query_lower for word in ["chicken", "poultry"])
        }
    
    def _matches_dietary_constraints(self, query: str, constraints: Dict[str, bool], meal_tags: list, meal_name: str, meal_ingredients: list, similarity: float) -> bool:
        """Check if meal matches dietary constraints from query"""
        query_lower = query.lower()
        
        # If searching for vegetarian, exclude non-vegetarian
        if constraints["vegetarian"]:
            # Check if meal is explicitly vegetarian
            if any(tag.lower() == "vegetarian" for tag in meal_tags):
                return True
            # Check ingredients for meat/fish
            non_veg_keywords = ["chicken", "fish", "seafood", "meat", "beef", "pork", "lamb", "prawn", "shrimp", "salmon"]
            if any(keyword in meal_name or any(keyword in ing for ing in meal_ingredients) for keyword in non_veg_keywords):
                return False
            # High similarity for veg query
            return similarity > 0.25
        
        # If searching for seafood, prefer seafood meals
        if constraints["seafood"]:
            seafood_keywords = ["fish", "seafood", "shrimp", "prawn", "salmon", "tuna", "crab", "lobster"]
            has_seafood = any(keyword in meal_name or any(keyword in ing for ing in meal_ingredients) for keyword in seafood_keywords)
            if has_seafood:
                return True
            # Exclude if vegetarian and looking for seafood
            if any(tag.lower() == "vegetarian" for tag in meal_tags):
                return False
            return similarity > 0.3
        
        # If searching for chicken, prefer chicken meals
        if constraints["chicken"]:
            chicken_keywords = ["chicken", "poultry"]
            has_chicken = any(keyword in meal_name or any(keyword in ing for ing in meal_ingredients) for keyword in chicken_keywords)
            if has_chicken:
                return True
            # Exclude vegetarian if specifically looking for chicken
            if any(tag.lower() == "vegetarian" for tag in meal_tags):
                return False
            return similarity > 0.3
        
        # If searching for non-veg (but not specific type)
        if constraints["non_veg"]:
            # Exclude vegetarian meals
            if any(tag.lower() == "vegetarian" for tag in meal_tags):
                return False
            return similarity > 0.25
        
        # Default: accept if good similarity
        return similarity > 0.25
    
    def generate_rag_context(self, meals: List[Dict[str, Any]]) -> str:
        """
        Generate context string from retrieved meals for LLM prompt
        
        Args:
            meals: List of retrieved meals
            
        Returns:
            Formatted context string
        """
        if not meals:
            return "No relevant meals found in the database."
        
        context_parts = ["Here are relevant meals from our database:"]
        for meal in meals:
            part = f"\n- {meal['name']}: {meal['description']}"
            if meal.get('ingredients'):
                part += f" (Ingredients: {', '.join(meal['ingredients'][:3])})"
            context_parts.append(part)
        
        return "\n".join(context_parts)
    
    def answer_query(self, query: str, top_k: int = 5, collection_name: str = "meals") -> RAGResponse:
        """
        Answer user query using RAG approach
        
        Args:
            query: User query
            top_k: Number of meals to retrieve
            collection_name: Collection to search
            
        Returns:
            RAG response with answer and retrieved meals
        """
        # Retrieve relevant meals
        meals = self.retrieve_relevant_meals(query, top_k, collection_name)
        
        # Create context for answer generation
        context = self.generate_rag_context(meals)
        
        # Simple answer generation (can be enhanced with LLM)
        answer = self._generate_answer(query, context, meals)
        
        # Calculate average confidence
        avg_confidence = sum([m['relevance_score'] for m in meals]) / len(meals) if meals else 0.0
        
        # Format results
        retrieved_results = [
            MealRetrievalResult(
                meal_name=m['name'],
                description=m['description'],
                relevance_score=m['relevance_score'],
                source=m['source']
            )
            for m in meals
        ]
        
        return RAGResponse(
            answer=answer,
            retrieved_meals=retrieved_results,
            confidence=min(avg_confidence, 1.0)
        )
    
    def _generate_answer(self, query: str, context: str, meals: List[Dict[str, Any]]) -> str:
        """
        Generate answer based on query and retrieved context using LLM
        
        Args:
            query: User query
            context: Context from retrieved meals
            meals: Retrieved meal objects
            
        Returns:
            Generated answer
        """
        if not meals:
            return f"I couldn't find relevant meals matching your query '{query}'. Please try a different search."
        
        # Create detailed meal information for LLM
        meal_details = []
        for i, meal in enumerate(meals, 1):
            detail = f"{i}. {meal['name']} (Source: {meal['source']}, Relevance: {meal['relevance_score']:.2%})\n"
            detail += f"   Description: {meal['description']}\n"
            if meal.get('ingredients'):
                detail += f"   Ingredients: {', '.join(meal['ingredients'][:5])}\n"
            if meal.get('instructions'):
                detail += f"   Instructions: {meal['instructions'][:150]}...\n"
            meal_details.append(detail)
        
        meals_info = "\n".join(meal_details)
        
        # Use LLM to generate answer with better analysis
        prompt = f"""You are an expert meal recommendation assistant. Analyze the user's query and the provided meals carefully.

USER QUERY: \"{query}\"

MEALS FROM DATABASE:
{meals_info}

ANALYSIS INSTRUCTIONS:
1. Carefully read the user's query and identify key requirements (dietary restrictions, time, health goals, cuisine, etc.)
2. Evaluate each meal against the user's query requirements
3. Identify which meals truly match the query and which don't
4. Provide specific reasons why meals match or don't match
5. Filter out meals that don't match well
6. Recommend only the best matches with detailed explanations
7. Suggest why these meals are good choices for the user's needs

RESPONSE FORMAT:
- Start with a brief summary of what the user is looking for
- List only the meals that best match their requirements with explanations
- Explain why each meal is a good choice
- If no meals match well, suggest alternatives or explain the limitation
- Keep response under 250 words but be thorough in analysis"""
        
        try:
            answer = self.llm_service.generate_answer(prompt, max_tokens=500)
            return answer
        except Exception as e:
            print(f"Error generating answer with LLM: {str(e)}")
            return f"Based on your query about '{query}', I found {len(meals)} relevant meal(s).\n\n{context}"
