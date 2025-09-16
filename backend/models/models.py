"""
SQLAlchemy models for the Blue Carbon MRV Platform
Defines database schema for users, projects, MRV reports, and carbon credits
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database.database import Base
import uuid

class User(Base):
    """User model for authentication and role management"""
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    name = Column(String, nullable=False)
    organization = Column(String, nullable=False)
    role = Column(String, nullable=False)  # ngo, auditor, corporate, government
    is_active = Column(Boolean, default=True)
    wallet_address = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    projects = relationship("Project", back_populates="owner")
    mrv_reports = relationship("MRVReport", back_populates="auditor")

class Project(Base):
    """Blue carbon restoration project model"""
    __tablename__ = "projects"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    location = Column(String, nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    project_type = Column(String, nullable=False)  # mangroves, seagrass, salt_marshes
    area_hectares = Column(Float, nullable=False)
    start_date = Column(DateTime, nullable=False)
    status = Column(String, default="active")  # active, completed, suspended
    owner_id = Column(String, ForeignKey("users.id"), nullable=False)
    baseline_data = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    owner = relationship("User", back_populates="projects")
    mrv_reports = relationship("MRVReport", back_populates="project")
    monitoring_data = relationship("MonitoringData", back_populates="project")

class MonitoringData(Base):
    """Monitoring data uploads for projects"""
    __tablename__ = "monitoring_data"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = Column(String, ForeignKey("projects.id"), nullable=False)
    data_type = Column(String, nullable=False)  # satellite, field_measurement, photo
    file_path = Column(String, nullable=True)
    data_content = Column(JSON, nullable=True)
    collection_date = Column(DateTime, nullable=False)
    metadata = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    project = relationship("Project", back_populates="monitoring_data")

class MRVReport(Base):
    """MRV (Monitoring, Reporting, Verification) reports"""
    __tablename__ = "mrv_reports"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = Column(String, ForeignKey("projects.id"), nullable=False)
    report_period_start = Column(DateTime, nullable=False)
    report_period_end = Column(DateTime, nullable=False)
    co2_sequestered_tons = Column(Float, nullable=False)
    biomass_tons = Column(Float, nullable=True)
    methodology = Column(String, nullable=False)
    confidence_score = Column(Float, nullable=True)
    ml_analysis_results = Column(JSON, nullable=True)
    status = Column(String, default="pending")  # pending, under_review, approved, rejected
    auditor_id = Column(String, ForeignKey("users.id"), nullable=True)
    auditor_notes = Column(Text, nullable=True)
    verification_date = Column(DateTime, nullable=True)
    ipfs_hash = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    project = relationship("Project", back_populates="mrv_reports")
    auditor = relationship("User", back_populates="mrv_reports")
    carbon_credits = relationship("CarbonCredit", back_populates="mrv_report")

class CarbonCredit(Base):
    """Carbon credits minted from verified MRV reports"""
    __tablename__ = "carbon_credits"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    token_id = Column(Integer, unique=True, nullable=False)
    mrv_report_id = Column(String, ForeignKey("mrv_reports.id"), nullable=False)
    total_supply = Column(Integer, nullable=False)
    available_supply = Column(Integer, nullable=False)
    price_per_credit = Column(Float, nullable=True)
    vintage_year = Column(Integer, nullable=False)
    project_type = Column(String, nullable=False)
    quality_grade = Column(String, default="standard")  # standard, premium
    blockchain_tx_hash = Column(String, nullable=True)
    contract_address = Column(String, nullable=True)
    is_retired = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    mrv_report = relationship("MRVReport", back_populates="carbon_credits")
    transactions = relationship("CreditTransaction", back_populates="carbon_credit")

class CreditTransaction(Base):
    """Carbon credit marketplace transactions"""
    __tablename__ = "credit_transactions"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    carbon_credit_id = Column(String, ForeignKey("carbon_credits.id"), nullable=False)
    buyer_id = Column(String, ForeignKey("users.id"), nullable=False)
    seller_id = Column(String, ForeignKey("users.id"), nullable=True)
    transaction_type = Column(String, nullable=False)  # purchase, retirement, transfer
    quantity = Column(Integer, nullable=False)
    price_per_credit = Column(Float, nullable=True)
    total_amount = Column(Float, nullable=True)
    blockchain_tx_hash = Column(String, nullable=True)
    status = Column(String, default="pending")  # pending, completed, failed
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    carbon_credit = relationship("CarbonCredit", back_populates="transactions")
    buyer = relationship("User", foreign_keys=[buyer_id])
    seller = relationship("User", foreign_keys=[seller_id])