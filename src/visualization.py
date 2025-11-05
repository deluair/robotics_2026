"""
Visualization Module for Robotics Industry Projections 2026

Creates charts and graphs for industry projections.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import os
import sys

# Handle imports for both package and direct execution
try:
    from .data_collection import RoboticsDataCollector
    from .analysis import RoboticsProjectionAnalyzer
except ImportError:
    # If running as script, add parent directory to path
    sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
    from src.data_collection import RoboticsDataCollector
    from src.analysis import RoboticsProjectionAnalyzer


class RoboticsVisualizer:
    """Creates visualizations for robotics industry data and projections."""
    
    def __init__(self, config_instance=None):
        """
        Initialize the visualizer.
        
        Args:
            config_instance: Optional custom configuration instance.
        """
        try:
            from .config import config as default_config
            from .logger_config import logger as default_logger
            from .data_collection import RoboticsDataCollector
            from .analysis import RoboticsProjectionAnalyzer
        except ImportError:
            import sys
            import os
            sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
            from src.config import config as default_config
            from src.logger_config import logger as default_logger
            from src.data_collection import RoboticsDataCollector
            from src.analysis import RoboticsProjectionAnalyzer
        
        self.config = config_instance or default_config
        self.logger = default_logger
        self.collector = RoboticsDataCollector(self.config)
        self.analyzer = RoboticsProjectionAnalyzer(self.config)
        self.output_dir = self.config.FIGURES_DIR
        
        # Set style
        plt.style.use('seaborn-v0_8-darkgrid')
        sns.set_palette("husl")
        
        self.logger.info("Initialized RoboticsVisualizer")
    
    def plot_global_market_trend(self, save=True):
        """Plot global market size trend with 2026 projection."""
        global_df, _, _ = self.collector.load_data()
        projections = self.analyzer.generate_2026_projections()
        
        # Extend dataframe with projection
        extended_years = list(global_df['year']) + [2026]
        extended_values = list(global_df['global_market_size']) + [
            projections['global_market_size']['ensemble']
        ]
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Historical data
        ax.plot(global_df['year'], global_df['global_market_size'], 
                'o-', linewidth=2, markersize=8, label='Historical Data', color='#2E86AB')
        
        # Projection
        ax.plot([2024, 2026], 
                [global_df['global_market_size'].iloc[-1], 
                 projections['global_market_size']['ensemble']],
                '--', linewidth=2, label='2026 Projection', color='#A23B72')
        
        ax.scatter([2026], [projections['global_market_size']['ensemble']],
                   s=150, color='#A23B72', zorder=5, marker='*')
        
        ax.set_xlabel('Year', fontsize=12, fontweight='bold')
        ax.set_ylabel('Market Size (Billion USD)', fontsize=12, fontweight='bold')
        ax.set_title('Global Robotics Market Size Trend (2015-2026)', 
                     fontsize=14, fontweight='bold', pad=20)
        ax.legend(fontsize=10)
        ax.grid(True, alpha=0.3)
        
        # Add value annotations
        for year, value in zip(global_df['year'][::2], 
                              global_df['global_market_size'][::2]):
            ax.annotate(f'${value:.1f}B', (year, value), 
                       textcoords="offset points", xytext=(0,10), 
                       ha='center', fontsize=8)
        
        ax.annotate(f'${projections["global_market_size"]["ensemble"]:.1f}B',
                   (2026, projections['global_market_size']['ensemble']),
                   textcoords="offset points", xytext=(0,15),
                   ha='center', fontsize=10, fontweight='bold', color='#A23B72')
        
        plt.tight_layout()
        
        if save:
            plt.savefig(os.path.join(self.output_dir, 'global_market_trend.png'),
                       dpi=300, bbox_inches='tight')
            print(f"Saved: {os.path.join(self.output_dir, 'global_market_trend.png')}")
        
        return fig
    
    def plot_regional_comparison(self, save=True):
        """Plot regional market comparison with 2026 projections."""
        _, regional_df, _ = self.collector.load_data()
        projections = self.analyzer.generate_2026_projections()
        
        regions = ['china', 'japan', 'south_korea', 'germany', 'usa', 'rest_of_world']
        region_names = {
            'china': 'China',
            'japan': 'Japan',
            'south_korea': 'South Korea',
            'germany': 'Germany',
            'usa': 'United States',
            'rest_of_world': 'Rest of World'
        }
        
        # 2024 values
        values_2024 = [regional_df[r].iloc[-1] for r in regions]
        # 2026 projections
        values_2026 = [projections[r]['ensemble'] for r in regions]
        
        x = np.arange(len(regions))
        width = 0.35
        
        fig, ax = plt.subplots(figsize=(14, 7))
        
        bars1 = ax.bar(x - width/2, values_2024, width, label='2024', color='#2E86AB')
        bars2 = ax.bar(x + width/2, values_2026, width, label='2026 Projection', color='#A23B72')
        
        ax.set_xlabel('Region', fontsize=12, fontweight='bold')
        ax.set_ylabel('Market Size (Billion USD)', fontsize=12, fontweight='bold')
        ax.set_title('Regional Robotics Market Comparison (2024 vs 2026)', 
                     fontsize=14, fontweight='bold', pad=20)
        ax.set_xticks(x)
        ax.set_xticklabels([region_names[r] for r in regions], rotation=45, ha='right')
        ax.legend(fontsize=10)
        ax.grid(True, alpha=0.3, axis='y')
        
        # Add value labels on bars
        for bars in [bars1, bars2]:
            for bar in bars:
                height = bar.get_height()
                ax.annotate(f'${height:.1f}B',
                           xy=(bar.get_x() + bar.get_width() / 2, height),
                           xytext=(0, 3),
                           textcoords="offset points",
                           ha='center', va='bottom', fontsize=8)
        
        plt.tight_layout()
        
        if save:
            plt.savefig(os.path.join(self.output_dir, 'regional_comparison.png'),
                       dpi=300, bbox_inches='tight')
            print(f"Saved: {os.path.join(self.output_dir, 'regional_comparison.png')}")
        
        return fig
    
    def plot_segment_breakdown(self, save=True):
        """Plot industry segment breakdown for 2026."""
        projections = self.analyzer.generate_2026_projections()
        
        segments = {
            'industrial_robots': 'Industrial Robots',
            'service_robots': 'Service Robots',
            'medical_robots': 'Medical Robots',
            'agricultural_robots': 'Agricultural Robots'
        }
        
        segment_values = [projections[s]['ensemble'] for s in segments.keys()]
        segment_labels = list(segments.values())
        
        colors = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D']
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
        
        # Pie chart
        wedges, texts, autotexts = ax1.pie(segment_values, labels=segment_labels,
                                          autopct='%1.1f%%', startangle=90,
                                          colors=colors, textprops={'fontsize': 10})
        ax1.set_title('Market Share by Segment (2026)', fontsize=14, fontweight='bold', pad=20)
        
        # Bar chart
        bars = ax2.barh(segment_labels, segment_values, color=colors)
        ax2.set_xlabel('Market Size (Billion USD)', fontsize=12, fontweight='bold')
        ax2.set_title('Market Size by Segment (2026)', fontsize=14, fontweight='bold', pad=20)
        ax2.grid(True, alpha=0.3, axis='x')
        
        # Add value labels
        for i, (bar, value) in enumerate(zip(bars, segment_values)):
            ax2.annotate(f'${value:.1f}B',
                        xy=(value, i),
                        xytext=(5, 0),
                        textcoords="offset points",
                        va='center', fontsize=10, fontweight='bold')
        
        plt.tight_layout()
        
        if save:
            plt.savefig(os.path.join(self.output_dir, 'segment_breakdown.png'),
                       dpi=300, bbox_inches='tight')
            print(f"Saved: {os.path.join(self.output_dir, 'segment_breakdown.png')}")
        
        return fig
    
    def plot_china_focus(self, save=True):
        """Create detailed visualization focusing on China's market position."""
        _, regional_df, installations_df = self.collector.load_data()
        projections = self.analyzer.generate_2026_projections()
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('China Market Growth Trend', 
                          'China vs Global Market Share',
                          'China Robot Installations',
                          'China vs Other Major Markets (2026)'),
            specs=[[{"type": "scatter"}, {"type": "pie"}],
                   [{"type": "scatter"}, {"type": "bar"}]]
        )
        
        # China market growth trend
        china_years = list(regional_df['year']) + [2026]
        china_values = list(regional_df['china']) + [projections['china']['ensemble']]
        
        fig.add_trace(
            go.Scatter(x=regional_df['year'], y=regional_df['china'],
                      mode='lines+markers', name='Historical',
                      line=dict(color='#C73E1D', width=3)),
            row=1, col=1
        )
        fig.add_trace(
            go.Scatter(x=[2024, 2026], 
                      y=[regional_df['china'].iloc[-1], projections['china']['ensemble']],
                      mode='lines+markers', name='Projection',
                      line=dict(color='#C73E1D', width=3, dash='dash'),
                      marker=dict(size=12)),
            row=1, col=1
        )
        
        # China vs Global market share pie
        china_share = projections['china']['ensemble']
        global_total = projections['global_market_size']['ensemble']
        rest_share = global_total - china_share
        
        fig.add_trace(
            go.Pie(labels=['China', 'Rest of World'],
                  values=[china_share, rest_share],
                  marker=dict(colors=['#C73E1D', '#2E86AB']),
                  textinfo='label+percent+value',
                  texttemplate='%{label}<br>$%{value:.1f}B<br>%{percent}'),
            row=1, col=2
        )
        
        # China installations trend
        china_inst_years = list(installations_df['year']) + [2026]
        china_inst_values = list(installations_df['china_installations']) + [
            projections['china_installations']['ensemble']
        ]
        
        fig.add_trace(
            go.Scatter(x=installations_df['year'], 
                      y=installations_df['china_installations'],
                      mode='lines+markers', name='Historical Installations',
                      line=dict(color='#F18F01', width=3),
                      showlegend=False),
            row=2, col=1
        )
        fig.add_trace(
            go.Scatter(x=[2024, 2026],
                      y=[installations_df['china_installations'].iloc[-1],
                        projections['china_installations']['ensemble']],
                      mode='lines+markers', name='Projected Installations',
                      line=dict(color='#F18F01', width=3, dash='dash'),
                      marker=dict(size=12),
                      showlegend=False),
            row=2, col=1
        )
        
        # China vs other markets bar chart
        major_markets = ['china', 'usa', 'japan', 'germany', 'south_korea']
        market_names = ['China', 'USA', 'Japan', 'Germany', 'South Korea']
        market_values = [projections[m]['ensemble'] for m in major_markets]
        
        fig.add_trace(
            go.Bar(x=market_names, y=market_values,
                  marker=dict(color=['#C73E1D' if m == 'china' else '#2E86AB' 
                                     for m in major_markets]),
                  text=[f'${v:.1f}B' for v in market_values],
                  textposition='outside'),
            row=2, col=2
        )
        
        # Update layout
        fig.update_layout(
            height=900,
            title_text="China Robotics Market Analysis (2026 Projections)",
            title_x=0.5,
            title_font_size=16,
            showlegend=True
        )
        
        fig.update_xaxes(title_text="Year", row=1, col=1)
        fig.update_yaxes(title_text="Market Size (Billion USD)", row=1, col=1)
        fig.update_xaxes(title_text="Year", row=2, col=1)
        fig.update_yaxes(title_text="Installations (Thousand Units)", row=2, col=1)
        fig.update_xaxes(title_text="Country", row=2, col=2)
        fig.update_yaxes(title_text="Market Size (Billion USD)", row=2, col=2)
        
        if save:
            output_path = os.path.join(self.output_dir, 'china_market_analysis.html')
            fig.write_html(output_path)
            print(f"Saved: {output_path}")
        
        return fig
    
    def create_all_visualizations(self):
        """Generate all visualizations."""
        print("Creating visualizations...")
        print("-" * 50)
        
        self.plot_global_market_trend()
        self.plot_regional_comparison()
        self.plot_segment_breakdown()
        self.plot_china_focus()
        
        print("-" * 50)
        print("All visualizations created successfully!")


if __name__ == "__main__":
    visualizer = RoboticsVisualizer()
    visualizer.create_all_visualizations()

