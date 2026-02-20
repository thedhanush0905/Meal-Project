from typing import Dict, Any, List
from models.schemas import RAGResponse


class ResponseValidator:
    """Service to validate AI responses"""
    
    def __init__(self):
        self.min_confidence = 0.3
        self.max_answer_length = 2000
    
    def validate_rag_response(self, response: RAGResponse) -> Dict[str, Any]:
        """
        Validate RAG response quality
        
        Args:
            response: RAG response to validate
            
        Returns:
            Validation result with issues and recommendations
        """
        issues = []
        warnings = []
        
        # Check confidence
        if response.confidence < self.min_confidence:
            warnings.append(f"Low confidence score: {response.confidence:.2f}")
        
        # Check retrieved meals
        if not response.retrieved_meals:
            issues.append("No meals retrieved")
        elif len(response.retrieved_meals) < 3:
            warnings.append(f"Only {len(response.retrieved_meals)} meals retrieved")
        
        # Check relevance scores
        avg_relevance = sum([m.relevance_score for m in response.retrieved_meals]) / len(response.retrieved_meals) if response.retrieved_meals else 0
        if avg_relevance < 0.5:
            warnings.append(f"Low average relevance score: {avg_relevance:.2f}")
        
        # Check answer length
        if len(response.answer) > self.max_answer_length:
            issues.append("Answer exceeds maximum length")
        
        if not response.answer or len(response.answer.strip()) == 0:
            issues.append("Empty answer")
        
        is_valid = len(issues) == 0
        
        return {
            "is_valid": is_valid,
            "issues": issues,
            "warnings": warnings,
            "quality_score": min(response.confidence, 1.0)
        }
    
    def validate_meal_data(self, meal_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate meal data before ingestion
        
        Args:
            meal_data: Meal data to validate
            
        Returns:
            Validation result
        """
        issues = []
        
        # Check required fields
        required_fields = ["name", "description", "ingredients", "instructions"]
        for field in required_fields:
            if field not in meal_data or not meal_data[field]:
                issues.append(f"Missing required field: {field}")
        
        # Check data types
        if "ingredients" in meal_data and not isinstance(meal_data["ingredients"], list):
            issues.append("Ingredients must be a list")
        
        if "name" in meal_data and len(str(meal_data["name"])) > 200:
            issues.append("Meal name too long (max 200 chars)")
        
        is_valid = len(issues) == 0
        
        return {
            "is_valid": is_valid,
            "issues": issues
        }
