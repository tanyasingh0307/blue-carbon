"""
Projects router for blue carbon restoration project management
Handles project CRUD operations, file uploads, and monitoring data
"""

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
import os
import uuid
import json
from datetime import datetime

from database.database import get_db
from models.models import Project, MonitoringData, User
from schemas.schemas import (
    ProjectCreate, Project as ProjectSchema, ProjectUpdate,
    MonitoringDataCreate, MonitoringData as MonitoringDataSchema
)
from routers.auth import get_current_user_dependency
from core.config import settings

router = APIRouter()

@router.post("/", response_model=ProjectSchema)
async def create_project(
    project_data: ProjectCreate,
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    """Create a new blue carbon restoration project"""
    
    # Only NGOs can create projects
    if current_user.role != "ngo":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only NGO users can create projects"
        )
    
    # Create project
    db_project = Project(
        name=project_data.name,
        description=project_data.description,
        location=project_data.location,
        latitude=project_data.latitude,
        longitude=project_data.longitude,
        project_type=project_data.project_type,
        area_hectares=project_data.area_hectares,
        start_date=project_data.start_date,
        owner_id=current_user.id,
        baseline_data=project_data.baseline_data
    )
    
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    
    return db_project

@router.get("/", response_model=List[ProjectSchema])
async def get_projects(
    skip: int = 0,
    limit: int = 100,
    project_type: Optional[str] = None,
    status: Optional[str] = None,
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    """Get list of projects with optional filtering"""
    
    query = db.query(Project)
    
    # Filter by user role
    if current_user.role == "ngo":
        # NGOs can only see their own projects
        query = query.filter(Project.owner_id == current_user.id)
    # Auditors, corporates, and government can see all projects
    
    # Apply filters
    if project_type:
        query = query.filter(Project.project_type == project_type)
    if status:
        query = query.filter(Project.status == status)
    
    projects = query.offset(skip).limit(limit).all()
    return projects

@router.get("/{project_id}", response_model=ProjectSchema)
async def get_project(
    project_id: str,
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    """Get a specific project by ID"""
    
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    # Check permissions
    if current_user.role == "ngo" and project.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this project"
        )
    
    return project

@router.put("/{project_id}", response_model=ProjectSchema)
async def update_project(
    project_id: str,
    project_update: ProjectUpdate,
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    """Update a project"""
    
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    # Check permissions - only project owner can update
    if project.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this project"
        )
    
    # Update fields
    update_data = project_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(project, field, value)
    
    db.commit()
    db.refresh(project)
    
    return project

@router.delete("/{project_id}")
async def delete_project(
    project_id: str,
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    """Delete a project"""
    
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    # Check permissions
    if project.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this project"
        )
    
    db.delete(project)
    db.commit()
    
    return {"message": "Project deleted successfully"}

@router.post("/{project_id}/monitoring-data", response_model=MonitoringDataSchema)
async def upload_monitoring_data(
    project_id: str,
    data_type: str = Form(...),
    collection_date: str = Form(...),
    metadata: str = Form(None),
    file: UploadFile = File(None),
    data_content: str = Form(None),
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    """Upload monitoring data for a project"""
    
    # Check if project exists and user has permission
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    if current_user.role == "ngo" and project.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to upload data for this project"
        )
    
    # Handle file upload
    file_path = None
    if file:
        # Create unique filename
        file_extension = os.path.splitext(file.filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = os.path.join(settings.UPLOAD_DIR, unique_filename)
        
        # Save file
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
    
    # Parse data content and metadata
    parsed_data_content = None
    if data_content:
        try:
            parsed_data_content = json.loads(data_content)
        except json.JSONDecodeError:
            parsed_data_content = {"raw_data": data_content}
    
    parsed_metadata = None
    if metadata:
        try:
            parsed_metadata = json.loads(metadata)
        except json.JSONDecodeError:
            parsed_metadata = {"notes": metadata}
    
    # Create monitoring data record
    monitoring_data = MonitoringData(
        project_id=project_id,
        data_type=data_type,
        file_path=file_path,
        data_content=parsed_data_content,
        collection_date=datetime.fromisoformat(collection_date),
        metadata=parsed_metadata
    )
    
    db.add(monitoring_data)
    db.commit()
    db.refresh(monitoring_data)
    
    return monitoring_data

@router.get("/{project_id}/monitoring-data", response_model=List[MonitoringDataSchema])
async def get_monitoring_data(
    project_id: str,
    data_type: Optional[str] = None,
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    """Get monitoring data for a project"""
    
    # Check project access
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    if current_user.role == "ngo" and project.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this project's data"
        )
    
    # Query monitoring data
    query = db.query(MonitoringData).filter(MonitoringData.project_id == project_id)
    
    if data_type:
        query = query.filter(MonitoringData.data_type == data_type)
    
    monitoring_data = query.order_by(MonitoringData.collection_date.desc()).all()
    return monitoring_data

@router.get("/stats/summary")
async def get_project_stats(
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    """Get project statistics summary"""
    
    query = db.query(Project)
    
    # Filter by user role
    if current_user.role == "ngo":
        query = query.filter(Project.owner_id == current_user.id)
    
    projects = query.all()
    
    # Calculate statistics
    total_projects = len(projects)
    total_area = sum(p.area_hectares for p in projects)
    project_types = {}
    
    for project in projects:
        project_type = project.project_type
        if project_type not in project_types:
            project_types[project_type] = 0
        project_types[project_type] += 1
    
    return {
        "total_projects": total_projects,
        "total_area_hectares": round(total_area, 2),
        "project_types": project_types,
        "active_projects": len([p for p in projects if p.status == "active"]),
        "completed_projects": len([p for p in projects if p.status == "completed"])
    }