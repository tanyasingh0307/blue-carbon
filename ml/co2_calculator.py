"""
Blue Carbon CO₂ Sequestration Calculator
Machine learning module for estimating carbon sequestration from blue carbon projects
"""

import numpy as np
import pandas as pd
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import json
import os

class BlueCarbonCalculator:
    """
    ML-powered calculator for blue carbon CO₂ sequestration
    Uses scientific literature and field data to estimate carbon storage
    """
    
    def __init__(self):
        self.sequestration_rates = {
            # Base rates in tons CO₂/hectare/year from scientific literature
            "mangroves": {
                "min": 4.2,
                "max": 12.8,
                "average": 6.8,
                "soil_factor": 0.85,  # Soil carbon contribution
                "biomass_factor": 0.15  # Above/below ground biomass
            },
            "seagrass": {
                "min": 2.1,
                "max": 7.4,
                "average": 4.2,
                "soil_factor": 0.90,
                "biomass_factor": 0.10
            },
            "salt_marshes": {
                "min": 1.8,
                "max": 6.2,
                "average": 3.5,
                "soil_factor": 0.80,
                "biomass_factor": 0.20
            }
        }
        
        self.environmental_factors = {
            "temperature": {"optimal": (20, 30), "weight": 0.15},
            "salinity": {"optimal": (15, 35), "weight": 0.10},
            "tidal_range": {"optimal": (0.5, 2.0), "weight": 0.12},
            "sediment_type": {"optimal": "organic_rich", "weight": 0.18},
            "water_quality": {"optimal": "good", "weight": 0.20},
            "vegetation_health": {"optimal": "excellent", "weight": 0.25}
        }
    
    def calculate_sequestration(
        self,
        project_type: str,
        area_hectares: float,
        age_years: float,
        environmental_data: Optional[Dict[str, Any]] = None,
        monitoring_data: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Calculate CO₂ sequestration for a blue carbon project
        
        Args:
            project_type: Type of blue carbon ecosystem
            area_hectares: Project area in hectares
            age_years: Age of the project in years
            environmental_data: Environmental conditions data
            monitoring_data: Field monitoring and satellite data
            
        Returns:
            Dictionary with sequestration estimates and metadata
        """
        
        if project_type.lower() not in self.sequestration_rates:
            raise ValueError(f"Unsupported project type: {project_type}")
        
        base_rates = self.sequestration_rates[project_type.lower()]
        
        # Base annual sequestration rate
        base_rate = base_rates["average"]
        
        # Apply age-based growth curve
        growth_factor = self._calculate_growth_factor(age_years, project_type)
        
        # Apply environmental factors
        env_factor = self._calculate_environmental_factor(environmental_data)
        
        # Apply monitoring data adjustments
        monitoring_factor = self._analyze_monitoring_data(monitoring_data, project_type)
        
        # Calculate total sequestration
        annual_rate = base_rate * growth_factor * env_factor * monitoring_factor
        total_sequestration = annual_rate * area_hectares
        
        # Calculate biomass components
        soil_carbon = total_sequestration * base_rates["soil_factor"]
        biomass_carbon = total_sequestration * base_rates["biomass_factor"]
        
        # Convert carbon to biomass (approximate)
        total_biomass = total_sequestration * 2.7  # C to biomass conversion
        
        # Calculate confidence score
        confidence = self._calculate_confidence(
            environmental_data, monitoring_data, age_years
        )
        
        # Prepare results
        results = {
            "co2_sequestered_tons": round(total_sequestration, 2),
            "biomass_tons": round(total_biomass, 2),
            "soil_carbon_tons": round(soil_carbon, 2),
            "biomass_carbon_tons": round(biomass_carbon, 2),
            "annual_rate_per_hectare": round(annual_rate, 2),
            "confidence_score": round(confidence, 1),
            "methodology": f"Blue Carbon ML Model v1.0 - {project_type}",
            "analysis_metadata": {
                "base_rate": base_rate,
                "growth_factor": round(growth_factor, 3),
                "environmental_factor": round(env_factor, 3),
                "monitoring_factor": round(monitoring_factor, 3),
                "project_age_years": age_years,
                "area_hectares": area_hectares,
                "calculation_date": datetime.utcnow().isoformat(),
                "data_sources": self._get_data_sources(monitoring_data)
            }
        }
        
        return results
    
    def _calculate_growth_factor(self, age_years: float, project_type: str) -> float:
        """Calculate growth factor based on project age and type"""
        
        if project_type.lower() == "mangroves":
            # Mangroves have slower initial growth but higher mature rates
            if age_years <= 1:
                return 0.2
            elif age_years <= 3:
                return 0.5
            elif age_years <= 5:
                return 0.8
            elif age_years <= 10:
                return 1.0
            else:
                return 1.1  # Mature mangroves can exceed average rates
        
        elif project_type.lower() == "seagrass":
            # Seagrass establishes quickly but plateaus
            if age_years <= 0.5:
                return 0.4
            elif age_years <= 2:
                return 0.9
            elif age_years <= 5:
                return 1.0
            else:
                return 0.95  # Slight decline in older beds
        
        elif project_type.lower() == "salt_marshes":
            # Salt marshes have steady growth
            if age_years <= 1:
                return 0.3
            elif age_years <= 3:
                return 0.7
            elif age_years <= 7:
                return 1.0
            else:
                return 1.0
        
        return 1.0  # Default
    
    def _calculate_environmental_factor(self, env_data: Optional[Dict[str, Any]]) -> float:
        """Calculate environmental adjustment factor"""
        
        if not env_data:
            return 1.0  # Neutral if no data
        
        total_weight = 0
        weighted_score = 0
        
        for factor, config in self.environmental_factors.items():
            if factor in env_data:
                value = env_data[factor]
                weight = config["weight"]
                score = self._score_environmental_factor(factor, value, config)
                
                weighted_score += score * weight
                total_weight += weight
        
        if total_weight == 0:
            return 1.0
        
        # Normalize to 0.7 - 1.3 range
        normalized_score = weighted_score / total_weight
        return 0.7 + (normalized_score * 0.6)
    
    def _score_environmental_factor(self, factor: str, value: Any, config: Dict) -> float:
        """Score individual environmental factor (0-1 scale)"""
        
        if factor in ["temperature", "salinity", "tidal_range"]:
            optimal_range = config["optimal"]
            if isinstance(value, (int, float)):
                if optimal_range[0] <= value <= optimal_range[1]:
                    return 1.0
                else:
                    # Distance from optimal range
                    if value < optimal_range[0]:
                        distance = optimal_range[0] - value
                    else:
                        distance = value - optimal_range[1]
                    
                    # Exponential decay
                    return max(0.1, np.exp(-distance / 10))
        
        elif factor == "sediment_type":
            sediment_scores = {
                "organic_rich": 1.0,
                "mixed": 0.8,
                "sandy": 0.6,
                "clay": 0.7,
                "rocky": 0.3
            }
            return sediment_scores.get(str(value).lower(), 0.5)
        
        elif factor in ["water_quality", "vegetation_health"]:
            quality_scores = {
                "excellent": 1.0,
                "good": 0.8,
                "fair": 0.6,
                "poor": 0.3,
                "very_poor": 0.1
            }
            return quality_scores.get(str(value).lower(), 0.5)
        
        return 0.5  # Default neutral score
    
    def _analyze_monitoring_data(
        self, 
        monitoring_data: Optional[List[Dict[str, Any]]], 
        project_type: str
    ) -> float:
        """Analyze monitoring data to adjust sequestration estimates"""
        
        if not monitoring_data:
            return 1.0
        
        adjustment_factor = 1.0
        data_quality_bonus = 0.0
        
        for data_point in monitoring_data:
            data_type = data_point.get("data_type", "")
            content = data_point.get("data_content", {})
            
            if data_type == "satellite":
                # Analyze satellite imagery data
                vegetation_coverage = content.get("vegetation_coverage_percent", 80)
                vegetation_health = content.get("vegetation_health", "good")
                change_rate = content.get("change_from_baseline_percent", 0)
                
                # Coverage adjustment
                if vegetation_coverage > 90:
                    adjustment_factor *= 1.1
                elif vegetation_coverage < 60:
                    adjustment_factor *= 0.8
                
                # Health adjustment
                health_multipliers = {
                    "excellent": 1.15,
                    "good": 1.0,
                    "fair": 0.85,
                    "poor": 0.6
                }
                adjustment_factor *= health_multipliers.get(vegetation_health, 1.0)
                
                # Growth trend adjustment
                if change_rate > 10:
                    adjustment_factor *= 1.1
                elif change_rate < -5:
                    adjustment_factor *= 0.9
                
                data_quality_bonus += 0.05
            
            elif data_type == "field_measurement":
                # Analyze field measurements
                tree_density = content.get("trees_per_hectare", 2000)
                avg_height = content.get("average_tree_height_m", 2.0)
                soil_carbon = content.get("soil_carbon_percent", 2.5)
                
                # Density adjustment for mangroves
                if project_type.lower() == "mangroves":
                    if tree_density > 3000:
                        adjustment_factor *= 1.1
                    elif tree_density < 1500:
                        adjustment_factor *= 0.9
                
                # Height adjustment
                if avg_height > 3.0:
                    adjustment_factor *= 1.05
                elif avg_height < 1.5:
                    adjustment_factor *= 0.95
                
                # Soil carbon adjustment
                if soil_carbon > 3.5:
                    adjustment_factor *= 1.1
                elif soil_carbon < 2.0:
                    adjustment_factor *= 0.9
                
                data_quality_bonus += 0.08
            
            elif data_type == "water_quality":
                # Water quality impact
                ph = content.get("ph", 7.5)
                dissolved_oxygen = content.get("dissolved_oxygen_mg_l", 6.0)
                turbidity = content.get("turbidity_ntu", 10)
                
                # pH adjustment
                if 7.0 <= ph <= 8.5:
                    adjustment_factor *= 1.02
                else:
                    adjustment_factor *= 0.98
                
                # Oxygen adjustment
                if dissolved_oxygen > 5.0:
                    adjustment_factor *= 1.02
                else:
                    adjustment_factor *= 0.95
                
                data_quality_bonus += 0.03
        
        # Apply data quality bonus (more data = higher confidence)
        final_adjustment = adjustment_factor * (1 + min(data_quality_bonus, 0.2))
        
        # Constrain to reasonable bounds
        return max(0.5, min(1.5, final_adjustment))
    
    def _calculate_confidence(
        self,
        env_data: Optional[Dict[str, Any]],
        monitoring_data: Optional[List[Dict[str, Any]]],
        age_years: float
    ) -> float:
        """Calculate confidence score for the estimate"""
        
        base_confidence = 75.0  # Base confidence
        
        # Age factor - more mature projects have higher confidence
        if age_years >= 3:
            base_confidence += 10
        elif age_years >= 1:
            base_confidence += 5
        else:
            base_confidence -= 5
        
        # Environmental data factor
        if env_data:
            data_completeness = len(env_data) / len(self.environmental_factors)
            base_confidence += data_completeness * 10
        
        # Monitoring data factor
        if monitoring_data:
            data_types = set(d.get("data_type", "") for d in monitoring_data)
            base_confidence += len(data_types) * 3
            
            # Recent data bonus
            recent_data = 0
            for data_point in monitoring_data:
                collection_date = data_point.get("collection_date")
                if collection_date:
                    try:
                        date = datetime.fromisoformat(collection_date.replace('Z', '+00:00'))
                        if (datetime.utcnow() - date).days <= 90:
                            recent_data += 1
                    except:
                        pass
            
            if recent_data > 0:
                base_confidence += min(recent_data * 2, 8)
        
        # Constrain to 70-98 range
        return max(70.0, min(98.0, base_confidence))
    
    def _get_data_sources(self, monitoring_data: Optional[List[Dict[str, Any]]]) -> List[str]:
        """Get list of data sources used in analysis"""
        
        if not monitoring_data:
            return ["baseline_model"]
        
        sources = set()
        for data_point in monitoring_data:
            data_type = data_point.get("data_type", "unknown")
            sources.add(data_type)
        
        return list(sources)
    
    def validate_project_data(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate project data and return validation results"""
        
        errors = []
        warnings = []
        
        # Required fields
        required_fields = ["project_type", "area_hectares", "start_date"]
        for field in required_fields:
            if field not in project_data:
                errors.append(f"Missing required field: {field}")
        
        # Validate project type
        if "project_type" in project_data:
            if project_data["project_type"].lower() not in self.sequestration_rates:
                errors.append(f"Unsupported project type: {project_data['project_type']}")
        
        # Validate area
        if "area_hectares" in project_data:
            area = project_data["area_hectares"]
            if not isinstance(area, (int, float)) or area <= 0:
                errors.append("Area must be a positive number")
            elif area > 10000:
                warnings.append("Very large project area - please verify")
        
        # Validate start date
        if "start_date" in project_data:
            try:
                start_date = datetime.fromisoformat(project_data["start_date"])
                if start_date > datetime.utcnow():
                    errors.append("Start date cannot be in the future")
                elif (datetime.utcnow() - start_date).days > 365 * 50:
                    warnings.append("Very old project - data may be less reliable")
            except:
                errors.append("Invalid start date format")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings
        }

# Example usage and testing
if __name__ == "__main__":
    calculator = BlueCarbonCalculator()
    
    # Example project data
    project_data = {
        "project_type": "mangroves",
        "area_hectares": 25.5,
        "start_date": "2022-01-15"
    }
    
    # Example environmental data
    env_data = {
        "temperature": 26.5,
        "salinity": 25.0,
        "tidal_range": 1.2,
        "sediment_type": "organic_rich",
        "water_quality": "good",
        "vegetation_health": "excellent"
    }
    
    # Example monitoring data
    monitoring_data = [
        {
            "data_type": "satellite",
            "data_content": {
                "vegetation_coverage_percent": 92,
                "vegetation_health": "excellent",
                "change_from_baseline_percent": 15
            },
            "collection_date": "2024-06-01"
        },
        {
            "data_type": "field_measurement",
            "data_content": {
                "trees_per_hectare": 2800,
                "average_tree_height_m": 2.8,
                "soil_carbon_percent": 3.2
            },
            "collection_date": "2024-05-15"
        }
    ]
    
    # Calculate age
    start_date = datetime.fromisoformat(project_data["start_date"])
    age_years = (datetime.utcnow() - start_date).days / 365.25
    
    # Run calculation
    results = calculator.calculate_sequestration(
        project_type=project_data["project_type"],
        area_hectares=project_data["area_hectares"],
        age_years=age_years,
        environmental_data=env_data,
        monitoring_data=monitoring_data
    )
    
    print("Blue Carbon Sequestration Analysis Results:")
    print(json.dumps(results, indent=2))