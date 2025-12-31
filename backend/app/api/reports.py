from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.review import Review

router = APIRouter()

@router.get("/{review_id}")
async def get_report(review_id: int, db: Session = Depends(get_db)):
    """Get the completed report for a review"""
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    
    # Return report details
    return {
        "review_id": review.id,
        "title": review.title,
        "status": review.status,
        "methodology": review.methodology,
        "research_question": review.research_question,
        "completed_at": review.completed_at
    }

@router.post("/{review_id}/generate")
async def generate_report(review_id: int, db: Session = Depends(get_db)):
    """Generate final report for a completed review"""
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    
    # In production, this would generate PDF/Word documents
    return {
        "message": "Report generation initiated",
        "review_id": review.id,
        "status": "processing"
    }
