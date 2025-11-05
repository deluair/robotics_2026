"""
Data Collection and Processing Module for Robotics Industry Projections 2026

This module handles data collection, cleaning, and preparation for analysis.
"""

import pandas as pd
import numpy as np
from typing import Tuple, Optional
from pathlib import Path

try:
    from .config import config
    from .logger_config import logger
except ImportError:
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent))
    from config import config
    from logger_config import logger


class RoboticsDataCollector:
    """
    Collects and processes robotics industry data.
    
    This class handles historical data generation, loading, and basic
    data processing operations for robotics market analysis.
    """
    
    def __init__(self, config_instance=None):
        """
        Initialize the data collector.
        
        Args:
            config_instance: Optional custom configuration instance.
                           If None, uses global config.
        """
        self.config = config_instance or config
        self.raw_dir = self.config.RAW_DATA_DIR
        self.processed_dir = self.config.PROCESSED_DATA_DIR
        
        logger.info(f"Initialized RoboticsDataCollector with data dir: {self.raw_dir}")
    
    def generate_historical_data(self) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """
        Generate realistic historical robotics industry data based on real trends.
        This simulates data collection from various sources.
        
        Returns:
            Tuple of (global_df, regional_df, installations_df)
            
        Raises:
            IOError: If data cannot be saved to disk
        """
        try:
            logger.info("Generating historical robotics industry data (2015-2024)")
            
            # Historical data: 2015-2024 (realistic estimates based on IFR data)
            years = list(range(2015, 2025))
            
            # Global market data (in billion USD)
            global_data = {
                'year': years,
                'global_market_size': [
                    24.8, 27.4, 31.1, 34.8, 38.2, 42.5, 47.8, 55.3, 63.2, 70.5
                ],
                'industrial_robots': [
                    18.5, 20.2, 22.8, 25.1, 27.3, 30.2, 33.8, 38.9, 44.2, 49.1
                ],
                'service_robots': [
                    3.2, 3.8, 4.5, 5.2, 6.1, 7.3, 8.5, 10.1, 12.0, 13.8
                ],
                'medical_robots': [
                    1.8, 2.1, 2.4, 2.8, 3.2, 3.6, 4.1, 4.7, 5.3, 6.0
                ],
                'agricultural_robots': [
                    1.3, 1.3, 1.4, 1.7, 1.6, 1.4, 1.4, 1.6, 1.7, 1.6
                ]
            }
            
            # Regional data (in billion USD)
            regional_data = {
                'year': years,
                'china': [
                    6.8, 8.2, 10.1, 12.3, 14.5, 16.8, 19.5, 22.8, 26.5, 29.8
                ],
                'japan': [
                    4.2, 4.5, 4.8, 5.1, 5.4, 5.7, 6.0, 6.4, 6.8, 7.2
                ],
                'south_korea': [
                    2.1, 2.3, 2.5, 2.7, 2.9, 3.1, 3.3, 3.5, 3.7, 3.9
                ],
                'germany': [
                    2.8, 3.0, 3.2, 3.4, 3.6, 3.8, 4.0, 4.3, 4.6, 4.9
                ],
                'usa': [
                    3.5, 3.8, 4.1, 4.4, 4.7, 5.0, 5.4, 5.8, 6.2, 6.6
                ],
                'rest_of_world': [
                    5.4, 5.6, 5.9, 6.3, 6.7, 7.1, 7.6, 8.2, 8.8, 9.5
                ]
            }
            
            # Robot installations (thousands of units)
            installations_data = {
                'year': years,
                'global_installations': [
                    254, 294, 340, 381, 422, 465, 517, 553, 610, 680
                ],
                'china_installations': [
                    68, 87, 138, 154, 181, 194, 214, 268, 290, 320
                ],
                'industrial_installations': [
                    253, 293, 339, 380, 421, 464, 516, 552, 609, 679
                ],
                'service_installations': [
                    5.4, 6.7, 8.2, 10.1, 12.5, 15.3, 18.7, 22.4, 26.8, 31.5
                ]
            }
            
            # Create DataFrames
            global_df = pd.DataFrame(global_data)
            regional_df = pd.DataFrame(regional_data)
            installations_df = pd.DataFrame(installations_data)
            
            # Validate data
            self._validate_dataframes(global_df, regional_df, installations_df)
            
            # Save to CSV
            global_path = self.config.get_raw_data_path(self.config.GLOBAL_MARKET_DATA_FILE)
            regional_path = self.config.get_raw_data_path(self.config.REGIONAL_MARKET_DATA_FILE)
            installations_path = self.config.get_raw_data_path(self.config.INSTALLATIONS_DATA_FILE)
            
            global_df.to_csv(global_path, index=False)
            regional_df.to_csv(regional_path, index=False)
            installations_df.to_csv(installations_path, index=False)
            
            logger.info(f"Historical data generated and saved to {self.raw_dir}")
            logger.debug(f"Global data shape: {global_df.shape}, "
                        f"Regional data shape: {regional_df.shape}, "
                        f"Installations data shape: {installations_df.shape}")
            
            return global_df, regional_df, installations_df
            
        except Exception as e:
            logger.error(f"Error generating historical data: {str(e)}", exc_info=True)
            raise
    
    def _validate_dataframes(
        self, 
        global_df: pd.DataFrame, 
        regional_df: pd.DataFrame, 
        installations_df: pd.DataFrame
    ) -> None:
        """
        Validate dataframes for required columns and data quality.
        
        Args:
            global_df: Global market dataframe
            regional_df: Regional market dataframe
            installations_df: Installations dataframe
            
        Raises:
            ValueError: If validation fails
        """
        required_global_cols = ['year', 'global_market_size', 'industrial_robots', 
                               'service_robots', 'medical_robots', 'agricultural_robots']
        required_regional_cols = ['year', 'china', 'japan', 'south_korea', 
                                 'germany', 'usa', 'rest_of_world']
        required_installations_cols = ['year', 'global_installations', 
                                      'china_installations', 'industrial_installations',
                                      'service_installations']
        
        for df, cols, name in [
            (global_df, required_global_cols, 'global'),
            (regional_df, required_regional_cols, 'regional'),
            (installations_df, required_installations_cols, 'installations')
        ]:
            missing_cols = set(cols) - set(df.columns)
            if missing_cols:
                raise ValueError(f"Missing columns in {name} dataframe: {missing_cols}")
            
            if df.isnull().any().any():
                logger.warning(f"Null values found in {name} dataframe")
            
            if len(df) == 0:
                raise ValueError(f"Empty {name} dataframe")
    
    def load_data(self) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """
        Load processed data from files.
        
        Returns:
            Tuple of (global_df, regional_df, installations_df)
            
        Raises:
            FileNotFoundError: If data files don't exist and can't be generated
            IOError: If data files can't be read
        """
        try:
            global_path = self.config.get_raw_data_path(self.config.GLOBAL_MARKET_DATA_FILE)
            regional_path = self.config.get_raw_data_path(self.config.REGIONAL_MARKET_DATA_FILE)
            installations_path = self.config.get_raw_data_path(self.config.INSTALLATIONS_DATA_FILE)
            
            if not all([global_path.exists(), regional_path.exists(), installations_path.exists()]):
                logger.warning("Data files not found. Generating historical data...")
                return self.generate_historical_data()
            
            logger.info("Loading historical data from files")
            global_df = pd.read_csv(global_path)
            regional_df = pd.read_csv(regional_path)
            installations_df = pd.read_csv(installations_path)
            
            logger.debug(f"Loaded data: {len(global_df)} records")
            return global_df, regional_df, installations_df
            
        except FileNotFoundError as e:
            logger.warning(f"Data files not found: {e}. Generating...")
            return self.generate_historical_data()
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}", exc_info=True)
            raise
    
    def calculate_growth_rates(self, df: pd.DataFrame, value_column: str) -> pd.DataFrame:
        """
        Calculate year-over-year growth rates and CAGR.
        
        Args:
            df: DataFrame with time series data
            value_column: Name of the column containing values
            
        Returns:
            DataFrame with added 'growth_rate' and 'cagr' columns
            
        Raises:
            ValueError: If value_column doesn't exist or df is empty
        """
        if value_column not in df.columns:
            raise ValueError(f"Column '{value_column}' not found in dataframe")
        
        if len(df) < 2:
            raise ValueError("DataFrame must have at least 2 rows to calculate growth rates")
        
        df = df.copy()
        df['growth_rate'] = df[value_column].pct_change() * 100
        
        if len(df) > 1 and df[value_column].iloc[0] > 0:
            years = len(df) - 1
            first_value = df[value_column].iloc[0]
            last_value = df[value_column].iloc[-1]
            df['cagr'] = ((last_value / first_value) ** (1 / years) - 1) * 100
        else:
            df['cagr'] = np.nan
        
        return df


if __name__ == "__main__":
    collector = RoboticsDataCollector()
    global_df, regional_df, installations_df = collector.generate_historical_data()
    
    print("\n=== Global Market Data ===")
    print(global_df.head(10))
    print("\n=== Regional Market Data ===")
    print(regional_df.head(10))
    print("\n=== Installations Data ===")
    print(installations_df.head(10))
