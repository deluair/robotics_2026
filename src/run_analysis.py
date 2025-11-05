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

try:
    from .data_collection import RoboticsDataCollector
    from .analysis import RoboticsProjectionAnalyzer
    from .visualization import RoboticsVisualizer
    from .dashboard import RoboticsDashboard
    from .logger_config import logger
    from .config import config
except ImportError:
    from data_collection import RoboticsDataCollector
    from analysis import RoboticsProjectionAnalyzer
    from visualization import RoboticsVisualizer
    from dashboard import RoboticsDashboard
    from logger_config import logger
    from config import config


def main():
    """Run the complete analysis pipeline."""
    logger.info("=" * 80)
    logger.info("ROBOTICS INDUSTRY PROJECTION ANALYSIS FOR 2026")
    logger.info("=" * 80)
    print("=" * 80)
    print("ROBOTICS INDUSTRY PROJECTION ANALYSIS FOR 2026")
    print("=" * 80)
    print()
    
    # Step 1: Data Collection
    logger.info("STEP 1: Data Collection and Processing")
    print("STEP 1: Data Collection and Processing")
    print("-" * 80)
    collector = RoboticsDataCollector(config)
    global_df, regional_df, installations_df = collector.generate_historical_data()
    logger.info(f"Historical data loaded: {len(global_df)} years of data")
    print(f"[OK] Historical data loaded: {len(global_df)} years of data")
    print()
    
    # Step 2: Analysis and Projections
    logger.info("STEP 2: Generating 2026 Projections")
    print("STEP 2: Generating 2026 Projections")
    print("-" * 80)
    analyzer = RoboticsProjectionAnalyzer(config)
    projections = analyzer.generate_2026_projections()
    logger.info("Projections generated using ensemble methods")
    print("[OK] Projections generated using ensemble methods")
    print()
    
    # Step 3: Save Projections
    logger.info("STEP 3: Saving Projections")
    print("STEP 3: Saving Projections")
    print("-" * 80)
    projection_df = analyzer.save_projections(projections)
    logger.info("Projections saved to CSV")
    print("[OK] Projections saved to CSV")
    print()
    
    # Step 4: Generate Report
    logger.info("STEP 4: Generating Report")
    print("STEP 4: Generating Report")
    print("-" * 80)
    report = analyzer.create_projection_report(projections)
    print(report)
    
    # Save report
    report_path = config.get_report_path(config.REPORT_FILE)
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    logger.info(f"Report saved to: {report_path}")
    print(f"\n[OK] Report saved to: {report_path}")
    print()
    
    # Step 5: Create Visualizations
    logger.info("STEP 5: Creating Visualizations")
    print("STEP 5: Creating Visualizations")
    print("-" * 80)
    visualizer = RoboticsVisualizer(config)
    visualizer.create_all_visualizations()
    logger.info("Visualizations created")
    print()
    
    # Step 6: Create Interactive Dashboards
    logger.info("STEP 6: Creating Interactive Dashboards")
    print("STEP 6: Creating Interactive Dashboards")
    print("-" * 80)
    dashboard = RoboticsDashboard(config)
    dashboard.save_dashboard('comprehensive')
    dashboard.save_dashboard('executive')
    logger.info("Dashboards created")
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

