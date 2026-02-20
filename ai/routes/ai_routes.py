from fastapi import APIRouter, HTTPException, status
from typing import List
from models.schemas import MealData, IngestionRequest, QueryRequest, RAGResponse
from services.meal_ai_service import MealAIService
from services.response_validator import ResponseValidator
from services.error_handler import ErrorHandler

router = APIRouter(prefix="/api/ai", tags=["AI"])

# Lazy-loaded services
_meal_ai_service = None
_response_validator = None
_error_handler = None

def get_meal_ai_service():
    global _meal_ai_service
    if _meal_ai_service is None:
        _meal_ai_service = MealAIService()
    return _meal_ai_service

def get_response_validator():
    global _response_validator
    if _response_validator is None:
        _response_validator = ResponseValidator()
    return _response_validator

def get_error_handler():
    global _error_handler
    if _error_handler is None:
        _error_handler = ErrorHandler()
    return _error_handler

# Convenience getters
meal_ai_service = get_meal_ai_service
response_validator = get_response_validator
error_handler = get_error_handler


@router.post("/ingest", summary="Ingest new meals into ChromaDB")
async def ingest_meals(request: IngestionRequest):
    """
    Ingest new meals from backend into ChromaDB.
    Called when user adds a meal through the backend.
    
    - **meals**: List of meals to ingest
    - **collection_name**: Name of collection (default: "meals")
    """
    try:
        # Validate meals
        validator = response_validator()
        handler = error_handler()
        service = meal_ai_service()
        
        for meal in request.meals:
            validation_result = validator.validate_meal_data(meal.dict())
            if not validation_result["is_valid"]:
                return handler.handle_validation_error(validation_result["issues"])
        
        # Ingest meals
        result = service.add_meals_batch(request.meals, request.collection_name)
        
        if result["success"]:
            return {
                "success": True,
                "message": f"Successfully ingested {result['meal_count']} meal(s)",
                "data": result
            }
        else:
            return handler.handle_ingestion_error(Exception(result["error"]))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/query", response_model=RAGResponse, summary="Query meals using RAG")
async def query_meals(request: QueryRequest):
    """
    Query meals using Retrieval-Augmented Generation.
    Retrieves relevant meals from ChromaDB and generates answer.
    
    - **prompt**: User's question about meals
    - **top_k**: Number of meals to retrieve (default: 5)
    - **collection_name**: Collection to search (default: "meals")
    """
    try:
        validator = response_validator()
        service = meal_ai_service()
        
        # Answer query
        response = service.answer_meal_query(
            request.prompt,
            request.top_k,
            request.collection_name
        )
        
        # Validate response
        validation = validator.validate_rag_response(response)
        
        if not validation["is_valid"] and validation["issues"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Response validation failed: {validation['issues']}"
            )
        
        return response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/stats/{collection_name}", summary="Get collection statistics")
async def get_collection_stats(collection_name: str = "meals"):
    """
    Get statistics about a collection in ChromaDB.
    
    - **collection_name**: Name of collection (default: "meals")
    """
    try:
        service = meal_ai_service()
        stats = service.get_collection_status(collection_name)
        
        if stats["success"]:
            return {
                "success": True,
                "data": stats
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Collection '{collection_name}' not found"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/single-meal", summary="Ingest a single meal")
async def add_single_meal(meal: MealData):
    """
    Ingest a single meal into ChromaDB.
    Convenience endpoint for adding individual meals.
    
    - **meal**: Meal data to add
    """
    try:
        validator = response_validator()
        handler = error_handler()
        service = meal_ai_service()
        
        # Validate meal
        validation_result = validator.validate_meal_data(meal.dict())
        if not validation_result["is_valid"]:
            return handler.handle_validation_error(validation_result["issues"])
        
        # Ingest meal
        result = service.add_user_meal(meal)
        
        if result["success"]:
            return {
                "success": True,
                "message": f"Successfully added meal: {meal.name}",
                "meal_id": result["meal_ids"][0] if result["meal_ids"] else None
            }
        else:
            return handler.handle_ingestion_error(Exception(result["error"]))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/populate-from-mealdb", summary="Populate ChromaDB with MealDB data")
async def populate_from_mealdb(count: int = 20, collection_name: str = "meals"):
    """
    Fetch meals from MealDB API and populate ChromaDB.
    This will add a rich dataset for better RAG results.
    
    - **count**: Number of meals to fetch (default: 20)
    - **collection_name**: Collection to populate (default: "meals")
    """
    try:
        from services.mealdb_service import MealDBService
        
        mealdb_service = MealDBService()
        service = meal_ai_service()
        
        print(f"Fetching {count} meals from MealDB API...")
        
        # Fetch popular meals from various categories
        meals = mealdb_service.fetch_popular_meals()
        
        if not meals:
            raise Exception("Failed to fetch meals from MealDB API")
        
        # Limit to requested count
        meals = meals[:count]
        
        print(f"Ingesting {len(meals)} meals into ChromaDB...")
        
        # Ingest into ChromaDB
        result = service.add_meals_batch(meals, collection_name)
        
        if result["success"]:
            return {
                "success": True,
                "message": f"Successfully populated ChromaDB with {result.get('meal_count', len(meals))} meals from MealDB",
                "meals_added": result.get('meal_count', len(meals)),
                "data": result
            }
        else:
            raise Exception(result.get("error", "Failed to ingest meals"))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error populating from MealDB: {str(e)}"
        )

