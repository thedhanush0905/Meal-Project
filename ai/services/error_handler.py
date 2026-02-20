from typing import Dict, Any
from fastapi.responses import JSONResponse
from fastapi import status


class ErrorHandler:
    """Centralized error handling for AI service"""
    
    @staticmethod
    def handle_ingestion_error(error: Exception) -> Dict[str, Any]:
        """
        Handle ingestion errors
        
        Args:
            error: Exception from ingestion
            
        Returns:
            Error response
        """
        return {
            "success": False,
            "error_type": "IngestionError",
            "message": str(error),
            "suggestion": "Please check your meal data and try again"
        }
    
    @staticmethod
    def handle_retrieval_error(error: Exception) -> Dict[str, Any]:
        """
        Handle retrieval errors
        
        Args:
            error: Exception from retrieval
            
        Returns:
            Error response
        """
        return {
            "success": False,
            "error_type": "RetrievalError",
            "message": str(error),
            "suggestion": "Please try a different query"
        }
    
    @staticmethod
    def handle_validation_error(errors: list) -> Dict[str, Any]:
        """
        Handle validation errors
        
        Args:
            errors: List of validation errors
            
        Returns:
            Error response
        """
        return {
            "success": False,
            "error_type": "ValidationError",
            "errors": errors,
            "message": "Data validation failed"
        }
    
    @staticmethod
    def create_error_response(status_code: int, error_type: str, message: str, details: Dict[str, Any] = None) -> JSONResponse:
        """
        Create formatted error response
        
        Args:
            status_code: HTTP status code
            error_type: Type of error
            message: Error message
            details: Additional details
            
        Returns:
            JSONResponse with error details
        """
        response_data = {
            "success": False,
            "error_type": error_type,
            "message": message
        }
        if details:
            response_data["details"] = details
        
        return JSONResponse(
            status_code=status_code,
            content=response_data
        )
