"""
Command Line Interface for Robotics Industry Projections 2026

Provides a CLI for running analysis, generating reports, and creating dashboards.
"""

import argparse
import sys
from pathlib import Path
from typing import Optional

try:
    from .run_analysis import main as run_full_analysis
    from .data_collection import RoboticsDataCollector
    from .analysis import RoboticsProjectionAnalyzer
    from .visualization import RoboticsVisualizer
    from .dashboard import RoboticsDashboard
    from .logger_config import logger
    from .config import config
except ImportError:
    import sys
    sys.path.insert(0, str(Path(__file__).parent))
    from run_analysis import main as run_full_analysis
    from data_collection import RoboticsDataCollector
    from analysis import RoboticsProjectionAnalyzer
    from visualization import RoboticsVisualizer
    from dashboard import RoboticsDashboard
    from logger_config import logger
    from config import config


def cmd_run_analysis(args: argparse.Namespace) -> int:
    """Run full analysis pipeline."""
    try:
        logger.info("Running full analysis pipeline")
        run_full_analysis()
        return 0
    except Exception as e:
        logger.error(f"Error running analysis: {e}", exc_info=True)
        return 1


def cmd_generate_data(args: argparse.Namespace) -> int:
    """Generate historical data."""
    try:
        logger.info("Generating historical data")
        collector = RoboticsDataCollector()
        global_df, regional_df, installations_df = collector.generate_historical_data()
        print(f"\nGenerated data:")
        print(f"  - Global: {len(global_df)} records")
        print(f"  - Regional: {len(regional_df)} records")
        print(f"  - Installations: {len(installations_df)} records")
        return 0
    except Exception as e:
        logger.error(f"Error generating data: {e}", exc_info=True)
        return 1


def cmd_projections(args: argparse.Namespace) -> int:
    """Generate projections only."""
    try:
        logger.info("Generating projections")
        analyzer = RoboticsProjectionAnalyzer()
        projections = analyzer.generate_2026_projections()
        
        # Save projections
        projection_df = analyzer.save_projections(projections)
        
        # Generate report
        if args.report:
            report = analyzer.create_projection_report(projections)
            print(report)
        
        return 0
    except Exception as e:
        logger.error(f"Error generating projections: {e}", exc_info=True)
        return 1


def cmd_visualize(args: argparse.Namespace) -> int:
    """Create visualizations."""
    try:
        logger.info("Creating visualizations")
        visualizer = RoboticsVisualizer()
        visualizer.create_all_visualizations()
        return 0
    except Exception as e:
        logger.error(f"Error creating visualizations: {e}", exc_info=True)
        return 1


def cmd_dashboard(args: argparse.Namespace) -> int:
    """Create dashboards."""
    try:
        logger.info("Creating dashboards")
        dashboard = RoboticsDashboard()
        
        if args.type == 'all' or args.type == 'comprehensive':
            dashboard.save_dashboard('comprehensive')
        if args.type == 'all' or args.type == 'executive':
            dashboard.save_dashboard('executive')
        
        return 0
    except Exception as e:
        logger.error(f"Error creating dashboards: {e}", exc_info=True)
        return 1


def create_parser() -> argparse.ArgumentParser:
    """Create and configure argument parser."""
    parser = argparse.ArgumentParser(
        description="Robotics Industry Projections 2026 - CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run full analysis
  robotics-2026 run

  # Generate projections with report
  robotics-2026 projections --report

  # Create only dashboards
  robotics-2026 dashboard --type comprehensive

  # Generate data only
  robotics-2026 data
        """
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version=f'robotics-industry-projections-2026 {config.VERSION}'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose logging'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Run command
    run_parser = subparsers.add_parser('run', help='Run full analysis pipeline')
    run_parser.set_defaults(func=cmd_run_analysis)
    
    # Data command
    data_parser = subparsers.add_parser('data', help='Generate historical data')
    data_parser.set_defaults(func=cmd_generate_data)
    
    # Projections command
    proj_parser = subparsers.add_parser('projections', help='Generate projections')
    proj_parser.add_argument(
        '--report',
        action='store_true',
        help='Print projection report to console'
    )
    proj_parser.set_defaults(func=cmd_projections)
    
    # Visualize command
    viz_parser = subparsers.add_parser('visualize', help='Create visualizations')
    viz_parser.set_defaults(func=cmd_visualize)
    
    # Dashboard command
    dash_parser = subparsers.add_parser('dashboard', help='Create interactive dashboards')
    dash_parser.add_argument(
        '--type',
        choices=['comprehensive', 'executive', 'all'],
        default='all',
        help='Dashboard type to create (default: all)'
    )
    dash_parser.set_defaults(func=cmd_dashboard)
    
    return parser


def main(args: Optional[list] = None) -> int:
    """
    Main entry point for CLI.
    
    Args:
        args: Optional command line arguments (for testing)
        
    Returns:
        Exit code (0 for success, non-zero for error)
    """
    import logging
    
    parser = create_parser()
    parsed_args = parser.parse_args(args)
    
    # Set logging level
    if parsed_args.verbose:
        logger.setLevel(logging.DEBUG)
    
    # Execute command
    if not parsed_args.command:
        parser.print_help()
        return 1
    
    try:
        return parsed_args.func(parsed_args)
    except KeyboardInterrupt:
        logger.info("Interrupted by user")
        return 130
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    import logging
    sys.exit(main())

