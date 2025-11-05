"""
Main execution script for Robotics Industry Projection Analysis 2026

This script runs the complete analysis pipeline:
1. Data collection and processing
2. Statistical analysis and projections
3. Visualization generation
4. Report generation
"""

import os
import sys

# Add src directory to path
sys.path.insert(0, os.path.dirname(__file__))

from data_collection import RoboticsDataCollector
from analysis import RoboticsProjectionAnalyzer
from visualization import RoboticsVisualizer
from dashboard import RoboticsDashboard


def main():
    """Run the complete analysis pipeline."""
    print("=" * 80)
    print("ROBOTICS INDUSTRY PROJECTION ANALYSIS FOR 2026")
    print("=" * 80)
    print()
    
    # Step 1: Data Collection
    print("STEP 1: Data Collection and Processing")
    print("-" * 80)
    collector = RoboticsDataCollector()
    global_df, regional_df, installations_df = collector.generate_historical_data()
    print(f"[OK] Historical data loaded: {len(global_df)} years of data")
    print()
    
    # Step 2: Analysis and Projections
    print("STEP 2: Generating 2026 Projections")
    print("-" * 80)
    analyzer = RoboticsProjectionAnalyzer()
    projections = analyzer.generate_2026_projections()
    print("[OK] Projections generated using ensemble methods")
    print()
    
    # Step 3: Save Projections
    print("STEP 3: Saving Projections")
    print("-" * 80)
    projection_df = analyzer.save_projections(projections)
    print("[OK] Projections saved to CSV")
    print()
    
    # Step 4: Generate Report
    print("STEP 4: Generating Report")
    print("-" * 80)
    report = analyzer.create_projection_report(projections)
    print(report)
    
    # Save report
    report_path = os.path.join(
        os.path.dirname(__file__), '..', 'outputs', 'reports', 'projection_report_2026.txt'
    )
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"\n[OK] Report saved to: {report_path}")
    print()
    
    # Step 5: Create Visualizations
    print("STEP 5: Creating Visualizations")
    print("-" * 80)
    visualizer = RoboticsVisualizer()
    visualizer.create_all_visualizations()
    print()
    
    # Step 6: Create Interactive Dashboards
    print("STEP 6: Creating Interactive Dashboards")
    print("-" * 80)
    dashboard = RoboticsDashboard()
    dashboard.save_dashboard('comprehensive')
    dashboard.save_dashboard('executive')
    print()
    
    print("=" * 80)
    print("ANALYSIS COMPLETE!")
    print("=" * 80)
    print("\nOutput files:")
    print(f"  - Projections CSV: data/processed/projections_2026.csv")
    print(f"  - Report: outputs/reports/projection_report_2026.txt")
    print(f"  - Visualizations: outputs/figures/")
    print(f"  - Interactive Dashboards: outputs/figures/robotics_dashboard_*.html")
    print()


if __name__ == "__main__":
    main()

