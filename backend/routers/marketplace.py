"""
Marketplace router for carbon credit trading
Handles buying, selling, and marketplace operations
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from database.database import get_db
from models.models import CarbonCredit, CreditTransaction, User, Project, MRVReport
from schemas.schemas import (
    PurchaseRequest, RetirementRequest, CreditTransaction as CreditTransactionSchema,
    MarketplaceFilter
)
from routers.auth import get_current_user_dependency
from services.blockchain_service import blockchain_service

router = APIRouter()

@router.get("/credits")
async def get_marketplace_credits(
    skip: int = 0,
    limit: int = 100,
    project_type: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    vintage_year: Optional[int] = None,
    quality_grade: Optional[str] = None,
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    """Get available carbon credits in the marketplace"""
    
    query = db.query(CarbonCredit).filter(
        CarbonCredit.available_supply > 0,
        CarbonCredit.is_retired == False,
        CarbonCredit.price_per_credit.isnot(None)
    )
    
    # Apply filters
    if project_type:
        query = query.filter(CarbonCredit.project_type == project_type)
    if min_price:
        query = query.filter(CarbonCredit.price_per_credit >= min_price)
    if max_price:
        query = query.filter(CarbonCredit.price_per_credit <= max_price)
    if vintage_year:
        query = query.filter(CarbonCredit.vintage_year == vintage_year)
    if quality_grade:
        query = query.filter(CarbonCredit.quality_grade == quality_grade)
    
    credits = query.offset(skip).limit(limit).order_by(CarbonCredit.created_at.desc()).all()
    
    # Enrich with project information
    enriched_credits = []
    for credit in credits:
        mrv_report = db.query(MRVReport).filter(MRVReport.id == credit.mrv_report_id).first()
        project = db.query(Project).filter(Project.id == mrv_report.project_id).first() if mrv_report else None
        
        credit_dict = {
            "id": credit.id,
            "token_id": credit.token_id,
            "total_supply": credit.total_supply,
            "available_supply": credit.available_supply,
            "price_per_credit": credit.price_per_credit,
            "vintage_year": credit.vintage_year,
            "project_type": credit.project_type,
            "quality_grade": credit.quality_grade,
            "blockchain_tx_hash": credit.blockchain_tx_hash,
            "created_at": credit.created_at,
            "project_name": project.name if project else "Unknown Project",
            "project_location": project.location if project else "Unknown Location",
            "co2_sequestered_tons": mrv_report.co2_sequestered_tons if mrv_report else 0,
            "verification_date": mrv_report.verification_date if mrv_report else None
        }
        enriched_credits.append(credit_dict)
    
    return enriched_credits

@router.post("/purchase", response_model=CreditTransactionSchema)
async def purchase_credits(
    purchase_request: PurchaseRequest,
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    """Purchase carbon credits from the marketplace"""
    
    # Only corporates and government can purchase credits
    if current_user.role not in ["corporate", "government"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only corporate and government users can purchase credits"
        )
    
    # Get carbon credit
    credit = db.query(CarbonCredit).filter(CarbonCredit.id == purchase_request.carbon_credit_id).first()
    if not credit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Carbon credit not found"
        )
    
    # Check availability
    if credit.available_supply < purchase_request.quantity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Insufficient credits available"
        )
    
    # Check price if specified
    if purchase_request.max_price_per_credit and credit.price_per_credit > purchase_request.max_price_per_credit:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Credit price exceeds maximum specified price"
        )
    
    # Calculate total amount
    total_amount = credit.price_per_credit * purchase_request.quantity if credit.price_per_credit else 0
    
    # Create transaction record
    transaction = CreditTransaction(
        carbon_credit_id=purchase_request.carbon_credit_id,
        buyer_id=current_user.id,
        transaction_type="purchase",
        quantity=purchase_request.quantity,
        price_per_credit=credit.price_per_credit,
        total_amount=total_amount,
        status="pending"
    )
    
    # Execute blockchain transfer (if applicable)
    try:
        # In a real implementation, this would transfer tokens to buyer's wallet
        # For now, we'll simulate the transaction
        
        # Update credit availability
        credit.available_supply -= purchase_request.quantity
        
        # Mark transaction as completed
        transaction.status = "completed"
        transaction.blockchain_tx_hash = f"0x{hash(str(transaction.id))}"  # Dummy hash
        
        db.add(transaction)
        db.commit()
        db.refresh(transaction)
        
        return transaction
    
    except Exception as e:
        transaction.status = "failed"
        db.add(transaction)
        db.commit()
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Purchase failed: {str(e)}"
        )

@router.post("/retire", response_model=CreditTransactionSchema)
async def retire_credits_marketplace(
    retirement_request: RetirementRequest,
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    """Retire carbon credits (permanent removal from circulation)"""
    
    # Only corporates and government can retire credits
    if current_user.role not in ["corporate", "government"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only corporate and government users can retire credits"
        )
    
    # Get carbon credit
    credit = db.query(CarbonCredit).filter(CarbonCredit.id == retirement_request.carbon_credit_id).first()
    if not credit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Carbon credit not found"
        )
    
    # Check if user has sufficient credits (in a real system, check wallet balance)
    if credit.available_supply < retirement_request.quantity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Insufficient credits available for retirement"
        )
    
    # Create retirement transaction
    transaction = CreditTransaction(
        carbon_credit_id=retirement_request.carbon_credit_id,
        buyer_id=current_user.id,
        transaction_type="retirement",
        quantity=retirement_request.quantity,
        status="pending"
    )
    
    try:
        # Execute blockchain retirement
        tx_hash = await blockchain_service.retire_credits(credit.token_id, retirement_request.quantity)
        
        # Update credit supply
        credit.available_supply -= retirement_request.quantity
        if credit.available_supply == 0:
            credit.is_retired = True
        
        # Update transaction
        transaction.status = "completed"
        transaction.blockchain_tx_hash = tx_hash or f"0x{hash(str(transaction.id))}"
        
        db.add(transaction)
        db.commit()
        db.refresh(transaction)
        
        return transaction
    
    except Exception as e:
        transaction.status = "failed"
        db.add(transaction)
        db.commit()
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Retirement failed: {str(e)}"
        )

@router.get("/transactions", response_model=List[CreditTransactionSchema])
async def get_user_transactions(
    skip: int = 0,
    limit: int = 100,
    transaction_type: Optional[str] = None,
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    """Get user's transaction history"""
    
    query = db.query(CreditTransaction).filter(CreditTransaction.buyer_id == current_user.id)
    
    if transaction_type:
        query = query.filter(CreditTransaction.transaction_type == transaction_type)
    
    transactions = query.offset(skip).limit(limit).order_by(CreditTransaction.created_at.desc()).all()
    return transactions

@router.get("/stats/market")
async def get_marketplace_stats(
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    """Get marketplace statistics"""
    
    # Available credits
    available_credits = db.query(CarbonCredit).filter(
        CarbonCredit.available_supply > 0,
        CarbonCredit.is_retired == False
    ).all()
    
    # All transactions
    transactions = db.query(CreditTransaction).filter(
        CreditTransaction.status == "completed"
    ).all()
    
    # Calculate statistics
    total_available_credits = sum(c.available_supply for c in available_credits)
    total_credits_with_price = sum(c.available_supply for c in available_credits if c.price_per_credit)
    
    # Price statistics
    priced_credits = [c for c in available_credits if c.price_per_credit]
    if priced_credits:
        prices = [c.price_per_credit for c in priced_credits]
        avg_price = sum(prices) / len(prices)
        min_price = min(prices)
        max_price = max(prices)
    else:
        avg_price = min_price = max_price = 0
    
    # Transaction volume
    purchase_transactions = [t for t in transactions if t.transaction_type == "purchase"]
    retirement_transactions = [t for t in transactions if t.transaction_type == "retirement"]
    
    total_volume = sum(t.total_amount for t in purchase_transactions if t.total_amount)
    total_purchased = sum(t.quantity for t in purchase_transactions)
    total_retired = sum(t.quantity for t in retirement_transactions)
    
    # Project type distribution
    project_types = {}
    for credit in available_credits:
        project_type = credit.project_type
        if project_type not in project_types:
            project_types[project_type] = 0
        project_types[project_type] += credit.available_supply
    
    return {
        "total_available_credits": total_available_credits,
        "total_credits_with_price": total_credits_with_price,
        "price_statistics": {
            "average_price": round(avg_price, 2),
            "min_price": round(min_price, 2),
            "max_price": round(max_price, 2)
        },
        "transaction_volume": {
            "total_volume_usd": round(total_volume, 2),
            "total_credits_purchased": total_purchased,
            "total_credits_retired": total_retired
        },
        "project_type_distribution": project_types,
        "active_listings": len(available_credits),
        "total_transactions": len(transactions)
    }

@router.get("/portfolio")
async def get_user_portfolio(
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    """Get user's carbon credit portfolio"""
    
    if current_user.role not in ["corporate", "government"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only corporate and government users have portfolios"
        )
    
    # Get user's transactions
    purchases = db.query(CreditTransaction).filter(
        CreditTransaction.buyer_id == current_user.id,
        CreditTransaction.transaction_type == "purchase",
        CreditTransaction.status == "completed"
    ).all()
    
    retirements = db.query(CreditTransaction).filter(
        CreditTransaction.buyer_id == current_user.id,
        CreditTransaction.transaction_type == "retirement",
        CreditTransaction.status == "completed"
    ).all()
    
    # Calculate portfolio
    total_purchased = sum(t.quantity for t in purchases)
    total_retired = sum(t.quantity for t in retirements)
    total_spent = sum(t.total_amount for t in purchases if t.total_amount)
    
    # Group by credit type
    credit_holdings = {}
    for transaction in purchases:
        credit_id = transaction.carbon_credit_id
        if credit_id not in credit_holdings:
            credit = db.query(CarbonCredit).filter(CarbonCredit.id == credit_id).first()
            credit_holdings[credit_id] = {
                "credit_id": credit_id,
                "token_id": credit.token_id if credit else None,
                "project_type": credit.project_type if credit else "Unknown",
                "vintage_year": credit.vintage_year if credit else None,
                "purchased_quantity": 0,
                "retired_quantity": 0,
                "total_spent": 0
            }
        
        credit_holdings[credit_id]["purchased_quantity"] += transaction.quantity
        credit_holdings[credit_id]["total_spent"] += transaction.total_amount or 0
    
    # Add retirement data
    for transaction in retirements:
        credit_id = transaction.carbon_credit_id
        if credit_id in credit_holdings:
            credit_holdings[credit_id]["retired_quantity"] += transaction.quantity
    
    # Calculate active holdings
    for holding in credit_holdings.values():
        holding["active_quantity"] = holding["purchased_quantity"] - holding["retired_quantity"]
    
    return {
        "summary": {
            "total_credits_purchased": total_purchased,
            "total_credits_retired": total_retired,
            "active_credits": total_purchased - total_retired,
            "total_spent_usd": round(total_spent, 2),
            "retirement_rate": round((total_retired / total_purchased * 100), 2) if total_purchased > 0 else 0
        },
        "holdings": list(credit_holdings.values()),
        "recent_transactions": len([t for t in purchases + retirements if (datetime.utcnow() - t.created_at).days <= 30])
    }