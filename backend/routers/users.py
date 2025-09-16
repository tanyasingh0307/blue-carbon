"""
Users router for user management and profile operations
Handles user CRUD operations and profile updates
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database.database import get_db
from models.models import User
from schemas.schemas import User as UserSchema, UserUpdate
from routers.auth import get_current_user_dependency

router = APIRouter()

@router.get("/me", response_model=UserSchema)
async def get_current_user_profile(
    current_user: User = Depends(get_current_user_dependency)
):
    """Get current user's profile"""
    return current_user

@router.put("/me", response_model=UserSchema)
async def update_current_user_profile(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    """Update current user's profile"""
    
    # Update fields
    update_data = user_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(current_user, field, value)
    
    db.commit()
    db.refresh(current_user)
    
    return current_user

@router.get("/", response_model=List[UserSchema])
async def get_users(
    skip: int = 0,
    limit: int = 100,
    role: str = None,
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    """Get list of users (admin/auditor access)"""
    
    # Only auditors and government users can view user lists
    if current_user.role not in ["auditor", "government"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view user list"
        )
    
    query = db.query(User)
    
    if role:
        query = query.filter(User.role == role)
    
    users = query.offset(skip).limit(limit).all()
    return users

@router.get("/{user_id}", response_model=UserSchema)
async def get_user(
    user_id: str,
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    """Get a specific user by ID"""
    
    # Users can only view their own profile, auditors and government can view any
    if current_user.id != user_id and current_user.role not in ["auditor", "government"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this user"
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user

@router.get("/stats/summary")
async def get_user_stats(
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    """Get user statistics summary"""
    
    # Only auditors and government can view user statistics
    if current_user.role not in ["auditor", "government"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view user statistics"
        )
    
    users = db.query(User).all()
    
    # Calculate statistics
    total_users = len(users)
    active_users = len([u for u in users if u.is_active])
    
    # Role distribution
    role_distribution = {}
    for user in users:
        role = user.role
        if role not in role_distribution:
            role_distribution[role] = 0
        role_distribution[role] += 1
    
    # Users with wallet addresses
    users_with_wallets = len([u for u in users if u.wallet_address])
    
    return {
        "total_users": total_users,
        "active_users": active_users,
        "inactive_users": total_users - active_users,
        "role_distribution": role_distribution,
        "users_with_wallets": users_with_wallets,
        "wallet_adoption_rate": round((users_with_wallets / total_users * 100), 2) if total_users > 0 else 0
    }