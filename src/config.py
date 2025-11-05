"""
Configuration Management for Robotics Industry Projections 2026

Centralized configuration for the entire project.
"""

import os
from pathlib import Path
from typing import Dict, Any
from dataclasses import dataclass


@dataclass
class ProjectConfig:
    """Project configuration settings."""
    
    # Project metadata
    PROJECT_NAME: str = "Robotics Industry Projections 2026"
    VERSION: str = "1.0.0"
    TARGET_YEAR: int = 2026
    
    # Paths
    PROJECT_ROOT: Path = Path(__file__).parent.parent
    DATA_DIR: Path = PROJECT_ROOT / "data"
    RAW_DATA_DIR: Path = DATA_DIR / "raw"
    PROCESSED_DATA_DIR: Path = DATA_DIR / "processed"
    OUTPUT_DIR: Path = PROJECT_ROOT / "outputs"
    FIGURES_DIR: Path = OUTPUT_DIR / "figures"
    REPORTS_DIR: Path = OUTPUT_DIR / "reports"
    
    # Data files
    GLOBAL_MARKET_DATA_FILE: str = "global_market_data.csv"
    REGIONAL_MARKET_DATA_FILE: str = "regional_market_data.csv"
    INSTALLATIONS_DATA_FILE: str = "installations_data.csv"
    PROJECTIONS_FILE: str = "projections_2026.csv"
    REPORT_FILE: str = "projection_report_2026.txt"
    
    # Dashboard files
    DASHBOARD_COMPREHENSIVE: str = "robotics_dashboard_comprehensive.html"
    DASHBOARD_EXECUTIVE: str = "robotics_dashboard_executive.html"
    
    # Forecasting parameters
    ENSEMBLE_WEIGHTS: Dict[str, float] = None
    
    # Visualization settings
    FIGURE_DPI: int = 300
    FIGURE_FORMAT: str = "png"
    DASHBOARD_HEIGHT: int = 1600
    EXECUTIVE_DASHBOARD_HEIGHT: int = 900
    
    # Color scheme
    COLORS: Dict[str, str] = None
    
    def __post_init__(self):
        """Initialize default values after dataclass initialization."""
        if self.ENSEMBLE_WEIGHTS is None:
            self.ENSEMBLE_WEIGHTS = {
                'linear': 0.2,
                'polynomial': 0.3,
                'exponential_smoothing': 0.2,
                'cagr': 0.3
            }
        
        if self.COLORS is None:
            self.COLORS = {
                'primary': '#2E86AB',
                'secondary': '#A23B72',
                'accent': '#F18F01',
                'success': '#06A77D',
                'warning': '#C73E1D',
                'china': '#C73E1D',
                'usa': '#2E86AB',
                'japan': '#F18F01',
                'germany': '#06A77D',
                'south_korea': '#A23B72'
            }
        
        # Create directories
        self._create_directories()
    
    def _create_directories(self):
        """Create necessary directories if they don't exist."""
        directories = [
            self.RAW_DATA_DIR,
            self.PROCESSED_DATA_DIR,
            self.FIGURES_DIR,
            self.REPORTS_DIR
        ]
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
    
    def get_raw_data_path(self, filename: str) -> Path:
        """Get full path to raw data file."""
        return self.RAW_DATA_DIR / filename
    
    def get_processed_data_path(self, filename: str) -> Path:
        """Get full path to processed data file."""
        return self.PROCESSED_DATA_DIR / filename
    
    def get_figure_path(self, filename: str) -> Path:
        """Get full path to figure file."""
        return self.FIGURES_DIR / filename
    
    def get_report_path(self, filename: str) -> Path:
        """Get full path to report file."""
        return self.REPORTS_DIR / filename


# Global configuration instance
config = ProjectConfig()

