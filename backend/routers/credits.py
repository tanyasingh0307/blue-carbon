"""
Carbon Credits router for blockchain token management
Handles credit minting, transfers, and retirement operations
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from database.database import get_db
from models.models import CarbonCredit, MRVReport, User, Project
from schemas.schemas import CarbonCreditCreate, CarbonCredit as CarbonCreditSchema
from routers.auth import get_current_user_dependency
from services.blockchain_service import blockchain_service

router = APIRouter()

@router.post("/mint", response_model=CarbonCreditSchema)
async def mint_carbon_credits(
    credit_data: CarbonCreditCreate,
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    """Mint carbon credits from verified MRV report (auditor only)"""
    
    # Only auditors can mint credits
    if current_user.role != "auditor":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only auditors can mint carbon credits"
        )
    
    # Check if MRV report exists and is approved
    mrv_report = db.query(MRVReport).filter(MRVReport.id == credit_data.mrv_report_id).first()
    if not mrv_report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="MRV report not found"
        )
    
    if mrv_report.status != "approved":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="MRV report must be approved before minting credits"
        )
    
    # Check if credits already exist for this report
    existing_credits = db.query(CarbonCredit).filter(
        CarbonCredit.mrv_report_id == credit_data.mrv_report_id
    ).first()
    if existing_credits:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Credits already minted for this MRV report"
        )
    
    # Get project information
    project = db.query(Project).filter(Project.id == mrv_report.project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Associated project not found"
        )
    
    # Generate unique token ID
    latest_credit = db.query(CarbonCredit).order_by(CarbonCredit.token_id.desc()).first()
    token_id = (latest_credit.token_id + 1) if latest_credit else 1
    
    # Calculate vintage year from report period
    vintage_year = mrv_report.report_period_end.year
    
    # Create carbon credit record
    carbon_credit = CarbonCredit(
        token_id=token_id,
        mrv_report_id=credit_data.mrv_report_id,
        total_supply=credit_data.total_supply,
        available_supply=credit_data.total_supply,
        price_per_credit=credit_data.price_per_credit,
        vintage_year=vintage_year,
        project_type=project.project_type,
        quality_grade=credit_data.quality_grade,
        contract_address=blockchain_service.contract.address if blockchain_service.contract else None
    )
    
    # Mint tokens on blockchain
    try:
        # Get project owner's wallet address (or use a default address)
        project_owner = db.query(User).filter(User.id == project.owner_id).first()
        to_address = project_owner.wallet_address if project_owner and project_owner.wallet_address else "0x0000000000000000000000000000000000000000"
        
        # Prepare metadata for blockchain
        metadata = {
            "project_name": project.name,
            "project_type": project.project_type,
            "co2_tons": mrv_report.co2_sequestered_tons,
            "vintage_year": vintage_year,
            "verification_date": mrv_report.verification_date.isoformat() if mrv_report.verification_date else None,
            "auditor_id": current_user.id
        }
        
        # Mint on blockchain
        tx_hash = await blockchain_service.mint_carbon_credits(
            to_address=to_address,
            token_id=token_id,
            amount=credit_data.total_supply,
            metadata=metadata
        )
        
        if tx_hash:
            carbon_credit.blockchain_tx_hash = tx_hash
        else:
            # If blockchain minting fails, still create the record but mark it
            print(f"Warning: Blockchain minting failed for token {token_id}")
    
    except Exception as e:
        print(f"Blockchain minting error: {e}")
        # Continue without blockchain integration for demo purposes
    
    # Save to database
    db.add(carbon_credit)
    db.commit()
    db.refresh(carbon_credit)
    
    return carbon_credit

@router.get("/", response_model=List[CarbonCreditSchema])
async def get_carbon_credits(
    skip: int = 0,
    limit: int = 100,
    project_type: Optional[str] = None,
    vintage_year: Optional[int] = None,
    available_only: bool = True,
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    """Get list of carbon credits with filtering"""
    
    query = db.query(CarbonCredit)
    
    # Apply filters
    if project_type:
        query = query.filter(CarbonCredit.project_type == project_type)
    if vintage_year:
        query = query.filter(CarbonCredit.vintage_year == vintage_year)
    if available_only:
        query = query.filter(CarbonCredit.available_supply > 0, CarbonCredit.is_retired == False)
    
    credits = query.offset(skip).limit(limit).order_by(CarbonCredit.created_at.desc()).all()
    return credits

@router.get("/{credit_id}", response_model=CarbonCreditSchema)
async def get_carbon_credit(
    credit_id: str,
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    """Get a specific carbon credit"""
    
    credit = db.query(CarbonCredit).filter(CarbonCredit.id == credit_id).first()
    if not credit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Carbon credit not found"
        )
    
    return credit

@router.post("/{credit_id}/retire")
async def retire_carbon_credits(
    credit_id: str,
    quantity: int,
    retirement_reason: Optional[str] = None,
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    """Retire carbon credits (remove from circulation)"""
    
    # Only corporates can retire credits (for now)
    if current_user.role not in ["corporate", "government"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only corporate users can retire carbon credits"
        )
    
    credit = db.query(CarbonCredit).filter(CarbonCredit.id == credit_id).first()
    if not credit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Carbon credit not found"
        )
    
    if credit.available_supply < quantity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Insufficient credits available for retirement"
        )
    
    # Retire on blockchain
    try:
        tx_hash = await blockchain_service.retire_credits(credit.token_id, quantity)
        
        # Update database
        credit.available_supply -= quantity
        if credit.available_supply == 0:
            credit.is_retired = True
        
        db.commit()
        
        return {
            "message": f"Successfully retired {quantity} carbon credits",
            "transaction_hash": tx_hash,
            "remaining_supply": credit.available_supply
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retire credits: {str(e)}"
        )

@router.get("/token/{token_id}/balance")
async def get_token_balance(
    token_id: int,
    address: str,
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    """Get token balance for a specific address"""
    
    try:
        balance = await blockchain_service.get_balance(address, token_id)
        return {
            "token_id": token_id,
            "address": address,
            "balance": balance
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get balance: {str(e)}"
        )

@router.get("/stats/summary")
async def get_credits_stats(
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    """Get carbon credits statistics"""
    
    credits = db.query(CarbonCredit).all()
    
    # Calculate statistics
    total_credits_minted = sum(c.total_supply for c in credits)
    total_credits_available = sum(c.available_supply for c in credits)
    total_credits_retired = total_credits_minted - total_credits_available
    
    # Project type distribution
    project_types = {}
    for credit in credits:
        project_type = credit.project_type
        if project_type not in project_types:
            project_types[project_type] = 0
        project_types[project_type] += credit.total_supply
    
    # Vintage year distribution
    vintage_years = {}
    for credit in credits:
        year = credit.vintage_year
        if year not in vintage_years:
            vintage_years[year] = 0
        vintage_years[year] += credit.total_supply
    
    # Average price
    priced_credits = [c for c in credits if c.price_per_credit is not None]
    avg_price = sum(c.price_per_credit for c in priced_credits) / len(priced_credits) if priced_credits else 0
    
    return {
        "total_credits_minted": total_credits_minted,
        "total_credits_available": total_credits_available,
        "total_credits_retired": total_credits_retired,
        "retirement_rate": round((total_credits_retired / total_credits_minted * 100), 2) if total_credits_minted > 0 else 0,
        "project_type_distribution": project_types,
        "vintage_year_distribution": vintage_years,
        "average_price_per_credit": round(avg_price, 2),
        "total_unique_tokens": len(credits)
    }