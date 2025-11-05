"""
Data Collection and Processing Module for Robotics Industry Projections 2026

This module handles data collection, cleaning, and preparation for analysis.
"""

import pandas as pd
import numpy as np
from datetime import datetime
import os


class RoboticsDataCollector:
    """Collects and processes robotics industry data."""
    
    def __init__(self):
        self.data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
        self.raw_dir = os.path.join(self.data_dir, 'raw')
        self.processed_dir = os.path.join(self.data_dir, 'processed')
        
        # Create directories if they don't exist
        os.makedirs(self.raw_dir, exist_ok=True)
        os.makedirs(self.processed_dir, exist_ok=True)
    
    def generate_historical_data(self):
        """
        Generate realistic historical robotics industry data based on real trends.
        This simulates data collection from various sources.
        """
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
        
        # Save to CSV
        global_df.to_csv(
            os.path.join(self.raw_dir, 'global_market_data.csv'),
            index=False
        )
        regional_df.to_csv(
            os.path.join(self.raw_dir, 'regional_market_data.csv'),
            index=False
        )
        installations_df.to_csv(
            os.path.join(self.raw_dir, 'installations_data.csv'),
            index=False
        )
        
        print(f"Historical data generated and saved to {self.raw_dir}")
        return global_df, regional_df, installations_df
    
    def load_data(self):
        """Load processed data from files."""
        try:
            global_df = pd.read_csv(
                os.path.join(self.raw_dir, 'global_market_data.csv')
            )
            regional_df = pd.read_csv(
                os.path.join(self.raw_dir, 'regional_market_data.csv')
            )
            installations_df = pd.read_csv(
                os.path.join(self.raw_dir, 'installations_data.csv')
            )
            return global_df, regional_df, installations_df
        except FileNotFoundError:
            print("Data files not found. Generating historical data...")
            return self.generate_historical_data()
    
    def calculate_growth_rates(self, df, value_column):
        """Calculate year-over-year growth rates."""
        df = df.copy()
        df['growth_rate'] = df[value_column].pct_change() * 100
        df['cagr'] = (
            (df[value_column].iloc[-1] / df[value_column].iloc[0]) ** 
            (1 / (len(df) - 1)) - 1
        ) * 100
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

