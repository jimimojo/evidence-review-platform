from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.review import Review, ReviewStatus, ReviewType
from app.models.user import User
from decimal import Decimal

router = APIRouter()

@router.post("/create")
async def create_review(
    title: str,
    description: str,
    review_type: ReviewType,
    research_question: str,
    methodology: str,
    price: float,
    client_id: int,
    db: Session = Depends(get_db)
):
    review = Review(
        title=title,
        description=description,
        review_type=review_type,
        research_question=research_question,
        methodology=methodology,
        price=Decimal(str(price)),
        client_id=client_id
    )
    db.add(review)
    db.commit()
    db.refresh(review)
    return {"message": "Review created successfully", "review_id": review.id}

@router.get("/list")
async def list_reviews(db: Session = Depends(get_db)):
    reviews = db.query(Review).all()
    return reviews

@router.get("/{review_id}")
async def get_review(review_id: int, db: Session = Depends(get_db)):
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review

@router.put("/{review_id}/status")
async def update_review_status(
    review_id: int,
    status: ReviewStatus,
    db: Session = Depends(get_db)
):
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    
    review.status = status
    db.commit()
    return {"message": "Review status updated", "status": status}

@router.put("/{review_id}/assign")
async def assign_reviewer(
    review_id: int,
    reviewer_id: int,
    db: Session = Depends(get_db)
):
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    
    reviewer = db.query(User).filter(User.id == reviewer_id).first()
    if not reviewer:
        raise HTTPException(status_code=404, detail="Reviewer not found")
    
    review.reviewer_id = reviewer_id
    review.status = ReviewStatus.IN_PROGRESS
    db.commit()
    return {"message": "Reviewer assigned successfully"}
