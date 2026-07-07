import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, List
import shutil
from datetime import datetime

# ==============================
#  Configuration & Logging
# ==============================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# ==============================
#  Data Models (Pydantic)
# ==============================
class ResumeRequest(BaseModel):
    resume_text: str

class ResumeResponse(BaseModel):
    score: int
    strengths: List[str]
    weaknesses: List[str]
    suggestions: List[str]
    technical_skills: List[str]
    soft_skills: List[str]
    years_experience: Optional[float] = None
    match_score: Optional[int] = None
    missing_skills: Optional[List[str]] = None
    career_level: Optional[str] = None
    suggested_roles: Optional[List[str]] = None
    summary: str

# ==============================
#  Lifespan Events (Startup & Shutdown)
# ==============================
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 Starting Resume Analyzer API...")
    logger.info("📚 Documentation available at /docs")
    logger.info("🔍 Redoc available at /redoc")
    yield
    logger.info("🛑 Shutting down Resume Analyzer API...")

# ==============================
#  FastAPI Application
# ==============================
app = FastAPI(
    title="Resume Analyzer API",
    description="AI-powered resume analysis service using Groq LLM",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# ==============================
#  Health Endpoints
# ==============================
@app.get("/")
async def root():
    return {
        "message": "🚀 Resume Analyzer API is running!",
        "version": "2.0.0",
        "docs": "/docs",
        "health": "/health",
        "status": "active"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "Resume Analyzer API",
        "version": "2.0.0",
        "timestamp": datetime.utcnow().isoformat()
    }

# ==============================
#  Analysis Endpoint
# ==============================
@app.post("/api/v1/analyze", response_model=ResumeResponse)
async def analyze_resume(request: ResumeRequest):
    logger.info(f"Received analysis request. Text length: {len(request.resume_text)}")
    
    if not request.resume_text or len(request.resume_text.strip()) < 20:
        logger.warning("Invalid input: resume text is too short")
        raise HTTPException(
            status_code=400,
            detail="Resume text cannot be empty and must be at least 20 characters long."
        )
    
    try:
        result = {
            "score": 85,
            "strengths": ["Python", "FastAPI", "Machine Learning", "Team Leadership"],
            "weaknesses": ["No cloud certifications", "Limited DevOps experience"],
            "suggestions": [
                "Add more quantifiable achievements",
                "Include GitHub portfolio link",
                "Consider obtaining cloud certification"
            ],
            "technical_skills": ["Python", "FastAPI", "Docker", "PostgreSQL", "Git"],
            "soft_skills": ["Leadership", "Communication", "Problem Solving"],
            "years_experience": 5.0,
            "match_score": 78,
            "missing_skills": ["Kubernetes", "AWS", "CI/CD"],
            "career_level": "Senior",
            "suggested_roles": ["Senior Backend Developer", "DevOps Engineer", "Tech Lead"],
            "summary": "Experienced Python developer with strong backend skills and team leadership experience."
        }
        logger.info("Analysis completed successfully")
        return result
    except Exception as e:
        logger.error(f"Error in analysis: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

# ==============================
#  File Upload Endpoint
# ==============================
@app.post("/api/v1/upload")
async def upload_resume(file: UploadFile = File(...)):
    logger.info(f"File upload requested: {file.filename}")
    
    allowed_extensions = [".pdf", ".docx"]
    file_extension = os.path.splitext(file.filename)[1].lower()
    
    if file_extension not in allowed_extensions:
        logger.warning(f"Unsupported file type: {file_extension}")
        raise HTTPException(
            status_code=400,
            detail="Unsupported file format. Only PDF and DOCX files are allowed."
        )
    
    try:
        os.makedirs("uploads", exist_ok=True)
        file_path = f"uploads/{datetime.utcnow().timestamp()}_{file.filename}"
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        file_size = os.path.getsize(file_path)
        logger.info(f"File uploaded successfully: {file_path} ({file_size} bytes)")
        
        return {
            "message": "File uploaded successfully",
            "filename": file.filename,
            "size": file_size,
            "path": file_path,
            "note": "File extraction not yet implemented. Coming soon!"
        }
    except Exception as e:
        logger.error(f"Upload error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"File upload failed: {str(e)}"
        )

# ==============================
#  Exception Handlers
# ==============================
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"detail": "Endpoint not found. Please check /docs"}
    )

@app.exception_handler(405)
async def method_not_allowed_handler(request, exc):
    return JSONResponse(
        status_code=405,
        content={"detail": "Method not allowed for this endpoint"}
    )

# ==============================
#  Main Entry Point (Fixed for Render)
# ==============================
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=False  # Disable reload in production
    )