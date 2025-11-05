"""
Tests for data collection module.
"""

import pytest
import pandas as pd
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from data_collection import RoboticsDataCollector
from config import config


class TestRoboticsDataCollector:
    """Test cases for RoboticsDataCollector."""
    
    def test_initialization(self):
        """Test collector initialization."""
        collector = RoboticsDataCollector()
        assert collector.config is not None
        assert collector.raw_dir.exists()
        assert collector.processed_dir.exists()
    
    def test_generate_historical_data(self):
        """Test historical data generation."""
        collector = RoboticsDataCollector()
        global_df, regional_df, installations_df = collector.generate_historical_data()
        
        # Check dataframes are created
        assert isinstance(global_df, pd.DataFrame)
        assert isinstance(regional_df, pd.DataFrame)
        assert isinstance(installations_df, pd.DataFrame)
        
        # Check required columns
        assert 'year' in global_df.columns
        assert 'global_market_size' in global_df.columns
        assert 'china' in regional_df.columns
        assert 'global_installations' in installations_df.columns
        
        # Check data ranges
        assert len(global_df) == 10  # 2015-2024
        assert global_df['year'].min() == 2015
        assert global_df['year'].max() == 2024
    
    def test_load_data(self):
        """Test data loading."""
        collector = RoboticsDataCollector()
        global_df, regional_df, installations_df = collector.load_data()
        
        assert isinstance(global_df, pd.DataFrame)
        assert isinstance(regional_df, pd.DataFrame)
        assert isinstance(installations_df, pd.DataFrame)
        assert len(global_df) > 0
    
    def test_calculate_growth_rates(self):
        """Test growth rate calculation."""
        collector = RoboticsDataCollector()
        df = pd.DataFrame({
            'year': [2020, 2021, 2022],
            'value': [100, 110, 121]
        })
        
        result = collector.calculate_growth_rates(df, 'value')
        assert 'growth_rate' in result.columns
        assert 'cagr' in result.columns
        assert not result['growth_rate'].isna().all()
    
    def test_calculate_growth_rates_error(self):
        """Test growth rate calculation with invalid input."""
        collector = RoboticsDataCollector()
        df = pd.DataFrame({'year': [2020], 'value': [100]})
        
        with pytest.raises(ValueError):
            collector.calculate_growth_rates(df, 'value')
        
        with pytest.raises(ValueError):
            collector.calculate_growth_rates(df, 'nonexistent_column')

