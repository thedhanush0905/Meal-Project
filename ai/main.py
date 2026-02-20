from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from routes.ai_routes import router as ai_router

# Load environment variables from .env file
load_dotenv(dotenv_path=".env")

# Create FastAPI app
app = FastAPI(
    title="Meal-Pro AI Service",
    description="AI service for Retrieval-Augmented Generation (RAG) of meal recommendations with Google Gemini",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(ai_router)


@app.get("/", tags=["Health"])
async def root():
    """Health check endpoint"""
    return {
        "service": "Meal-Pro AI",
        "status": "running",
        "version": "1.0.0",
        "llm": "Google Gemini"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check for deployment"""
    return {
        "status": "healthy",
        "service": "Meal-Pro AI"
    }


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("AI_PORT", 8001))
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=True,
        log_level="info"
    )
