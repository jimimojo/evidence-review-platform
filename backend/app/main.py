from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import reviews, auth, reports
from app.core.config import settings

app = FastAPI(
    title="Evidence Review Platform",
    description="Professional evidence synthesis and review management system",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["authentication"])
app.include_router(reviews.router, prefix="/api/reviews", tags=["reviews"])
app.include_router(reports.router, prefix="/api/reports", tags=["reports"])

@app.get("/")
async def root():
    return {
        "message": "Evidence Review Platform API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
