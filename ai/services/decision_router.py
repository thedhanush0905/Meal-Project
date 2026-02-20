from typing import Dict, Any
from enum import Enum


class RequestType(Enum):
    """Enum for request types"""
    MEAL_QUERY = "meal_query"
    MEAL_INGESTION = "meal_ingestion"
    COLLECTION_STAT = "collection_stat"
    UNKNOWN = "unknown"


class DecisionRouter:
    """Router to determine request type and route accordingly"""
    
    def __init__(self):
        self.keywords = {
            RequestType.MEAL_QUERY: ["recipe", "meal", "dish", "food", "ingredient", "cook", "make", "eat"],
            RequestType.MEAL_INGESTION: ["add", "ingest", "new meal", "save"],
            RequestType.COLLECTION_STAT: ["status", "count", "statistics", "how many"]
        }
    
    def route_request(self, text: str) -> Dict[str, Any]:
        """
        Determine request type and route
        
        Args:
            text: Input text/query
            
        Returns:
            Routing decision with type and confidence
        """
        text_lower = text.lower()
        
        request_scores = {}
        for req_type, keywords in self.keywords.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            request_scores[req_type] = score
        
        # Find best match
        best_match = max(request_scores, key=request_scores.get)
        max_score = request_scores[best_match]
        
        if max_score == 0:
            best_match = RequestType.UNKNOWN
        
        confidence = min(max_score / 3.0, 1.0)  # Normalize confidence
        
        return {
            "request_type": best_match.value,
            "confidence": confidence,
            "scores": {k.value: v for k, v in request_scores.items()}
        }
