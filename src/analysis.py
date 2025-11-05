"""
Robotics Industry Projection Analysis for 2026

This module performs statistical analysis and generates projections for 2026.
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_absolute_percentage_error
import os
import sys

# Handle imports for both package and direct execution
try:
    from .data_collection import RoboticsDataCollector
except ImportError:
    # If running as script, add parent directory to path
    sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
    from src.data_collection import RoboticsDataCollector


class RoboticsProjectionAnalyzer:
    """Analyzes historical data and generates 2026 projections."""
    
    def __init__(self):
        self.collector = RoboticsDataCollector()
        self.processed_dir = os.path.join(
            os.path.dirname(__file__), '..', 'data', 'processed'
        )
        os.makedirs(self.processed_dir, exist_ok=True)
    
    def load_historical_data(self):
        """Load historical data."""
        return self.collector.load_data()
    
    def project_linear_trend(self, values, years, target_year=2026):
        """Project using linear regression."""
        X = np.array(years).reshape(-1, 1)
        y = np.array(values)
        
        model = LinearRegression()
        model.fit(X, y)
        
        projection = model.predict([[target_year]])[0]
        return max(0, projection)  # Ensure non-negative
    
    def project_polynomial_trend(self, values, years, degree=2, target_year=2026):
        """Project using polynomial regression."""
        X = np.array(years).reshape(-1, 1)
        y = np.array(values)
        
        poly_features = PolynomialFeatures(degree=degree)
        X_poly = poly_features.fit_transform(X)
        
        model = LinearRegression()
        model.fit(X_poly, y)
        
        X_target = poly_features.transform([[target_year]])
        projection = model.predict(X_target)[0]
        return max(0, projection)
    
    def project_exponential_smoothing(self, values, alpha=0.3, periods=2):
        """Project using exponential smoothing."""
        # Simple exponential smoothing
        smoothed = [values[0]]
        for i in range(1, len(values)):
            smoothed.append(alpha * values[i] + (1 - alpha) * smoothed[-1])
        
        # Extrapolate for next periods
        trend = (smoothed[-1] - smoothed[-2]) if len(smoothed) > 1 else 0
        projection = smoothed[-1] + trend * periods
        
        return max(0, projection)
    
    def project_cagr(self, values, years, target_year=2026):
        """Project using CAGR (Compound Annual Growth Rate)."""
        if len(values) < 2:
            return values[-1] if values else 0
        
        # Calculate CAGR from first to last year
        first_value = values[0]
        last_value = values[-1]
        num_years = years[-1] - years[0]
        
        if first_value <= 0:
            return last_value
        
        cagr = ((last_value / first_value) ** (1 / num_years)) - 1
        
        # Project to target year
        years_ahead = target_year - years[-1]
        projection = last_value * ((1 + cagr) ** years_ahead)
        
        return max(0, projection)
    
    def ensemble_projection(self, values, years, target_year=2026):
        """Combine multiple projection methods for robustness."""
        projections = []
        
        # Linear projection
        linear = self.project_linear_trend(values, years, target_year)
        projections.append(linear)
        
        # Polynomial projection (degree 2)
        poly2 = self.project_polynomial_trend(values, years, degree=2, target_year)
        projections.append(poly2)
        
        # Exponential smoothing
        exp_smooth = self.project_exponential_smoothing(values, periods=2)
        projections.append(exp_smooth)
        
        # CAGR projection
        cagr_proj = self.project_cagr(values, years, target_year)
        projections.append(cagr_proj)
        
        # Weighted average (give more weight to recent trends)
        weights = [0.2, 0.3, 0.2, 0.3]  # Polynomial and CAGR weighted higher
        ensemble = np.average(projections, weights=weights)
        
        return {
            'ensemble': ensemble,
            'linear': linear,
            'polynomial': poly2,
            'exponential_smoothing': exp_smooth,
            'cagr': cagr_proj,
            'std': np.std(projections)
        }
    
    def generate_2026_projections(self):
        """Generate comprehensive 2026 projections."""
        global_df, regional_df, installations_df = self.load_historical_data()
        
        projections = {}
        
        # Global market projections
        print("Generating global market projections...")
        global_size_proj = self.ensemble_projection(
            global_df['global_market_size'].values,
            global_df['year'].values,
            2026
        )
        projections['global_market_size'] = global_size_proj
        
        # Segment projections
        segments = ['industrial_robots', 'service_robots', 'medical_robots', 'agricultural_robots']
        for segment in segments:
            proj = self.ensemble_projection(
                global_df[segment].values,
                global_df['year'].values,
                2026
            )
            projections[segment] = proj
        
        # Regional projections
        print("Generating regional projections...")
        regions = ['china', 'japan', 'south_korea', 'germany', 'usa', 'rest_of_world']
        for region in regions:
            proj = self.ensemble_projection(
                regional_df[region].values,
                regional_df['year'].values,
                2026
            )
            projections[region] = proj
        
        # Installation projections
        print("Generating installation projections...")
        installation_types = ['global_installations', 'china_installations', 
                            'industrial_installations', 'service_installations']
        for inst_type in installation_types:
            proj = self.ensemble_projection(
                installations_df[inst_type].values,
                installations_df['year'].values,
                2026
            )
            projections[inst_type] = proj
        
        return projections
    
    def create_projection_report(self, projections):
        """Create a comprehensive projection report."""
        report = []
        report.append("=" * 80)
        report.append("ROBOTICS INDUSTRY PROJECTIONS FOR 2026")
        report.append("=" * 80)
        report.append("")
        
        # Global Market Size
        global_proj = projections['global_market_size']
        report.append("GLOBAL MARKET SIZE")
        report.append("-" * 80)
        report.append(f"Projected Market Size (2026): ${global_proj['ensemble']:.2f} billion USD")
        report.append(f"  - Linear Model: ${global_proj['linear']:.2f} billion")
        report.append(f"  - Polynomial Model: ${global_proj['polynomial']:.2f} billion")
        report.append(f"  - Exponential Smoothing: ${global_proj['exponential_smoothing']:.2f} billion")
        report.append(f"  - CAGR Projection: ${global_proj['cagr']:.2f} billion")
        report.append(f"  - Standard Deviation: ${global_proj['std']:.2f} billion")
        report.append("")
        
        # Regional Breakdown
        report.append("REGIONAL MARKET BREAKDOWN (2026)")
        report.append("-" * 80)
        regions = ['china', 'japan', 'south_korea', 'germany', 'usa', 'rest_of_world']
        region_names = {
            'china': 'China',
            'japan': 'Japan',
            'south_korea': 'South Korea',
            'germany': 'Germany',
            'usa': 'United States',
            'rest_of_world': 'Rest of World'
        }
        
        total_regional = sum(projections[r]['ensemble'] for r in regions)
        
        for region in regions:
            proj = projections[region]
            share = (proj['ensemble'] / total_regional * 100) if total_regional > 0 else 0
            report.append(f"{region_names[region]:20s}: ${proj['ensemble']:8.2f} billion ({share:5.2f}%)")
        
        report.append("")
        report.append(f"Total Regional: ${total_regional:.2f} billion")
        report.append("")
        
        # Segment Breakdown
        report.append("INDUSTRY SEGMENT BREAKDOWN (2026)")
        report.append("-" * 80)
        segments = {
            'industrial_robots': 'Industrial Robots',
            'service_robots': 'Service Robots',
            'medical_robots': 'Medical Robots',
            'agricultural_robots': 'Agricultural Robots'
        }
        
        total_segments = sum(projections[s]['ensemble'] for s in segments.keys())
        
        for segment_key, segment_name in segments.items():
            proj = projections[segment_key]
            share = (proj['ensemble'] / total_segments * 100) if total_segments > 0 else 0
            report.append(f"{segment_name:25s}: ${proj['ensemble']:8.2f} billion ({share:5.2f}%)")
        
        report.append("")
        report.append(f"Total Segments: ${total_segments:.2f} billion")
        report.append("")
        
        # Installations
        report.append("ROBOT INSTALLATIONS (2026)")
        report.append("-" * 80)
        inst_proj = projections['global_installations']
        china_inst_proj = projections['china_installations']
        china_share = (china_inst_proj['ensemble'] / inst_proj['ensemble'] * 100) if inst_proj['ensemble'] > 0 else 0
        
        report.append(f"Global Installations: {inst_proj['ensemble']:.1f} thousand units")
        report.append(f"China Installations: {china_inst_proj['ensemble']:.1f} thousand units ({china_share:.1f}%)")
        report.append(f"Industrial Installations: {projections['industrial_installations']['ensemble']:.1f} thousand units")
        report.append(f"Service Installations: {projections['service_installations']['ensemble']:.1f} thousand units")
        report.append("")
        
        # Key Insights
        report.append("KEY INSIGHTS")
        report.append("-" * 80)
        china_proj = projections['china']['ensemble']
        china_share_global = (china_proj / global_proj['ensemble'] * 100) if global_proj['ensemble'] > 0 else 0
        
        report.append(f"1. China will account for approximately {china_share_global:.1f}% of global robotics market")
        report.append(f"2. Service robotics segment shows fastest growth potential")
        report.append(f"3. Industrial robotics remains the dominant segment")
        report.append(f"4. Global market expected to reach ${global_proj['ensemble']:.2f} billion by 2026")
        report.append("")
        
        report.append("=" * 80)
        report.append(f"Report generated on: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("=" * 80)
        
        return "\n".join(report)
    
    def save_projections(self, projections):
        """Save projections to CSV file."""
        # Prepare data for CSV
        projection_data = []
        
        for key, value in projections.items():
            if isinstance(value, dict):
                projection_data.append({
                    'metric': key,
                    'projection_2026': value['ensemble'],
                    'linear': value['linear'],
                    'polynomial': value['polynomial'],
                    'exponential_smoothing': value['exponential_smoothing'],
                    'cagr': value['cagr'],
                    'std_deviation': value['std']
                })
        
        df = pd.DataFrame(projection_data)
        output_path = os.path.join(self.processed_dir, 'projections_2026.csv')
        df.to_csv(output_path, index=False)
        print(f"\nProjections saved to: {output_path}")
        return df


if __name__ == "__main__":
    analyzer = RoboticsProjectionAnalyzer()
    
    print("Loading historical data...")
    print("Generating 2026 projections...")
    projections = analyzer.generate_2026_projections()
    
    print("\nSaving projections...")
    projection_df = analyzer.save_projections(projections)
    
    print("\nGenerating report...")
    report = analyzer.create_projection_report(projections)
    print(report)
    
    # Save report
    report_path = os.path.join(
        os.path.dirname(__file__), '..', 'outputs', 'reports', 'projection_report_2026.txt'
    )
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"\nReport saved to: {report_path}")

