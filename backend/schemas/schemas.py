"""
Pydantic schemas for request/response validation
Defines data models for API endpoints
"""

from pydantic import BaseModel, EmailStr, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

# Enums
class UserRole(str, Enum):
    NGO = "ngo"
    AUDITOR = "auditor"
    CORPORATE = "corporate"
    GOVERNMENT = "government"

class ProjectType(str, Enum):
    MANGROVES = "mangroves"
    SEAGRASS = "seagrass"
    SALT_MARSHES = "salt_marshes"

class ProjectStatus(str, Enum):
    ACTIVE = "active"
    COMPLETED = "completed"
    SUSPENDED = "suspended"

class MRVStatus(str, Enum):
    PENDING = "pending"
    UNDER_REVIEW = "under_review"
    APPROVED = "approved"
    REJECTED = "rejected"

# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    name: str
    organization: str
    role: UserRole

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    organization: Optional[str] = None
    wallet_address: Optional[str] = None

class User(UserBase):
    id: str
    is_active: bool
    wallet_address: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

# Authentication Schemas
class Token(BaseModel):
    access_token: str
    token_type: str
    user: User

class TokenData(BaseModel):
    email: Optional[str] = None

# Project Schemas
class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    location: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    project_type: ProjectType
    area_hectares: float
    start_date: datetime

class ProjectCreate(ProjectBase):
    baseline_data: Optional[Dict[str, Any]] = None

class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[ProjectStatus] = None
    baseline_data: Optional[Dict[str, Any]] = None

class Project(ProjectBase):
    id: str
    status: ProjectStatus
    owner_id: str
    baseline_data: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# Monitoring Data Schemas
class MonitoringDataCreate(BaseModel):
    data_type: str
    data_content: Optional[Dict[str, Any]] = None
    collection_date: datetime
    metadata: Optional[Dict[str, Any]] = None

class MonitoringData(MonitoringDataCreate):
    id: str
    project_id: str
    file_path: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

# MRV Report Schemas
class MRVReportCreate(BaseModel):
    report_period_start: datetime
    report_period_end: datetime
    methodology: str

class MRVReportUpdate(BaseModel):
    status: Optional[MRVStatus] = None
    auditor_notes: Optional[str] = None

class MRVReport(BaseModel):
    id: str
    project_id: str
    report_period_start: datetime
    report_period_end: datetime
    co2_sequestered_tons: float
    biomass_tons: Optional[float] = None
    methodology: str
    confidence_score: Optional[float] = None
    ml_analysis_results: Optional[Dict[str, Any]] = None
    status: MRVStatus
    auditor_id: Optional[str] = None
    auditor_notes: Optional[str] = None
    verification_date: Optional[datetime] = None
    ipfs_hash: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# Carbon Credit Schemas
class CarbonCreditCreate(BaseModel):
    mrv_report_id: str
    total_supply: int
    price_per_credit: Optional[float] = None
    quality_grade: str = "standard"

class CarbonCredit(BaseModel):
    id: str
    token_id: int
    mrv_report_id: str
    total_supply: int
    available_supply: int
    price_per_credit: Optional[float] = None
    vintage_year: int
    project_type: str
    quality_grade: str
    blockchain_tx_hash: Optional[str] = None
    contract_address: Optional[str] = None
    is_retired: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# Transaction Schemas
class CreditTransactionCreate(BaseModel):
    carbon_credit_id: str
    transaction_type: str
    quantity: int
    price_per_credit: Optional[float] = None

class CreditTransaction(BaseModel):
    id: str
    carbon_credit_id: str
    buyer_id: str
    seller_id: Optional[str] = None
    transaction_type: str
    quantity: int
    price_per_credit: Optional[float] = None
    total_amount: Optional[float] = None
    blockchain_tx_hash: Optional[str] = None
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True

# ML Analysis Schemas
class MLAnalysisRequest(BaseModel):
    project_id: str
    analysis_type: str = "co2_sequestration"
    parameters: Optional[Dict[str, Any]] = None

class MLAnalysisResult(BaseModel):
    co2_sequestered_tons: float
    biomass_tons: float
    confidence_score: float
    methodology: str
    analysis_metadata: Dict[str, Any]

# Marketplace Schemas
class MarketplaceFilter(BaseModel):
    project_type: Optional[ProjectType] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    vintage_year: Optional[int] = None
    quality_grade: Optional[str] = None

class PurchaseRequest(BaseModel):
    carbon_credit_id: str
    quantity: int
    max_price_per_credit: Optional[float] = None

class RetirementRequest(BaseModel):
    carbon_credit_id: str
    quantity: int
    retirement_reason: Optional[str] = None