"""
MRV (Monitoring, Reporting, Verification) router
Handles MRV report generation, ML analysis, and auditor verification
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta

from database.database import get_db
from models.models import Project, MRVReport, MonitoringData, User
from schemas.schemas import (
    MRVReportCreate, MRVReport as MRVReportSchema, MRVReportUpdate,
    MLAnalysisRequest, MLAnalysisResult
)
from routers.auth import get_current_user_dependency
from services.ml_service import ml_service

router = APIRouter()

@router.post("/{project_id}/generate-report", response_model=MRVReportSchema)
async def generate_mrv_report(
    project_id: str,
    report_data: MRVReportCreate,
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    """Generate MRV report with ML analysis for a project"""
    
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
            detail="Not authorized to generate reports for this project"
        )
    
    # Get monitoring data for the report period
    monitoring_data = db.query(MonitoringData).filter(
        MonitoringData.project_id == project_id,
        MonitoringData.collection_date >= report_data.report_period_start,
        MonitoringData.collection_date <= report_data.report_period_end
    ).all()
    
    if not monitoring_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No monitoring data available for the specified period"
        )
    
    # Prepare data for ML analysis
    project_data = {
        "project_type": project.project_type,
        "area_hectares": project.area_hectares,
        "start_date": project.start_date.isoformat(),
        "location": project.location,
        "baseline_data": project.baseline_data or {}
    }
    
    monitoring_data_list = []
    for data in monitoring_data:
        monitoring_data_list.append({
            "data_type": data.data_type,
            "data_content": data.data_content or {},
            "collection_date": data.collection_date.isoformat(),
            "metadata": data.metadata or {}
        })
    
    # Run ML analysis
    try:
        ml_results = ml_service.run_comprehensive_analysis(project_data, monitoring_data_list)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"ML analysis failed: {str(e)}"
        )
    
    # Create MRV report
    mrv_report = MRVReport(
        project_id=project_id,
        report_period_start=report_data.report_period_start,
        report_period_end=report_data.report_period_end,
        co2_sequestered_tons=ml_results["co2_sequestered_tons"],
        biomass_tons=ml_results.get("biomass_tons"),
        methodology=ml_results["methodology"],
        confidence_score=ml_results["confidence_score"],
        ml_analysis_results=ml_results,
        status="pending"
    )
    
    db.add(mrv_report)
    db.commit()
    db.refresh(mrv_report)
    
    return mrv_report

@router.get("/reports", response_model=List[MRVReportSchema])
async def get_mrv_reports(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    project_id: Optional[str] = None,
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    """Get MRV reports with filtering"""
    
    query = db.query(MRVReport)
    
    # Filter by user role
    if current_user.role == "ngo":
        # NGOs can only see reports for their projects
        user_projects = db.query(Project.id).filter(Project.owner_id == current_user.id).subquery()
        query = query.filter(MRVReport.project_id.in_(user_projects))
    elif current_user.role == "auditor":
        # Auditors can see all reports for verification
        pass
    elif current_user.role in ["corporate", "government"]:
        # Corporates and government can see approved reports
        query = query.filter(MRVReport.status == "approved")
    
    # Apply filters
    if status:
        query = query.filter(MRVReport.status == status)
    if project_id:
        query = query.filter(MRVReport.project_id == project_id)
    
    reports = query.offset(skip).limit(limit).order_by(MRVReport.created_at.desc()).all()
    return reports

@router.get("/reports/{report_id}", response_model=MRVReportSchema)
async def get_mrv_report(
    report_id: str,
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    """Get a specific MRV report"""
    
    report = db.query(MRVReport).filter(MRVReport.id == report_id).first()
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="MRV report not found"
        )
    
    # Check permissions
    if current_user.role == "ngo":
        project = db.query(Project).filter(Project.id == report.project_id).first()
        if not project or project.owner_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to view this report"
            )
    
    return report

@router.put("/reports/{report_id}/verify", response_model=MRVReportSchema)
async def verify_mrv_report(
    report_id: str,
    verification_data: MRVReportUpdate,
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    """Verify an MRV report (auditor only)"""
    
    # Only auditors can verify reports
    if current_user.role != "auditor":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only auditors can verify MRV reports"
        )
    
    report = db.query(MRVReport).filter(MRVReport.id == report_id).first()
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="MRV report not found"
        )
    
    if report.status not in ["pending", "under_review"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Report cannot be verified in its current status"
        )
    
    # Update report with verification
    report.status = verification_data.status or report.status
    report.auditor_id = current_user.id
    report.auditor_notes = verification_data.auditor_notes
    report.verification_date = datetime.utcnow()
    
    db.commit()
    db.refresh(report)
    
    return report

@router.post("/analyze", response_model=MLAnalysisResult)
async def run_ml_analysis(
    analysis_request: MLAnalysisRequest,
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    """Run ML analysis on project data"""
    
    # Check if project exists and user has permission
    project = db.query(Project).filter(Project.id == analysis_request.project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    if current_user.role == "ngo" and project.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to analyze this project"
        )
    
    # Get recent monitoring data
    recent_data = db.query(MonitoringData).filter(
        MonitoringData.project_id == analysis_request.project_id
    ).order_by(MonitoringData.collection_date.desc()).limit(10).all()
    
    # Prepare data for analysis
    project_data = {
        "project_type": project.project_type,
        "area_hectares": project.area_hectares,
        "start_date": project.start_date.isoformat(),
        "location": project.location
    }
    
    monitoring_data_list = []
    for data in recent_data:
        monitoring_data_list.append({
            "data_type": data.data_type,
            "data_content": data.data_content or {},
            "collection_date": data.collection_date.isoformat()
        })
    
    # Run analysis
    try:
        results = ml_service.run_comprehensive_analysis(project_data, monitoring_data_list)
        
        return MLAnalysisResult(
            co2_sequestered_tons=results["co2_sequestered_tons"],
            biomass_tons=results.get("biomass_tons", 0),
            confidence_score=results["confidence_score"],
            methodology=results["methodology"],
            analysis_metadata=results.get("analysis_metadata", {})
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis failed: {str(e)}"
        )

@router.get("/reports/stats/summary")
async def get_mrv_stats(
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    """Get MRV statistics summary"""
    
    query = db.query(MRVReport)
    
    # Filter by user role
    if current_user.role == "ngo":
        user_projects = db.query(Project.id).filter(Project.owner_id == current_user.id).subquery()
        query = query.filter(MRVReport.project_id.in_(user_projects))
    elif current_user.role in ["corporate", "government"]:
        query = query.filter(MRVReport.status == "approved")
    
    reports = query.all()
    
    # Calculate statistics
    total_reports = len(reports)
    total_co2_sequestered = sum(r.co2_sequestered_tons for r in reports)
    
    status_counts = {}
    for report in reports:
        status = report.status
        if status not in status_counts:
            status_counts[status] = 0
        status_counts[status] += 1
    
    # Recent activity (last 30 days)
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    recent_reports = [r for r in reports if r.created_at >= thirty_days_ago]
    
    return {
        "total_reports": total_reports,
        "total_co2_sequestered_tons": round(total_co2_sequestered, 2),
        "status_distribution": status_counts,
        "recent_reports_count": len(recent_reports),
        "average_confidence_score": round(
            sum(r.confidence_score for r in reports if r.confidence_score) / 
            len([r for r in reports if r.confidence_score]), 1
        ) if reports else 0
    }