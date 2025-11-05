"""
Comprehensive Interactive Dashboard for Robotics Industry Projections 2026

Creates a professional, interactive dashboard with multiple views and insights.
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import os
import sys
from datetime import datetime

# Handle imports
try:
    from .data_collection import RoboticsDataCollector
    from .analysis import RoboticsProjectionAnalyzer
except ImportError:
    sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
    from src.data_collection import RoboticsDataCollector
    from src.analysis import RoboticsProjectionAnalyzer


class RoboticsDashboard:
    """Creates comprehensive interactive dashboard for robotics projections."""
    
    def __init__(self, config_instance=None):
        """
        Initialize the dashboard creator.
        
        Args:
            config_instance: Optional custom configuration instance.
        """
        try:
            from .config import config as default_config
            from .logger_config import logger as default_logger
        except ImportError:
            import sys
            import os
            sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
            from src.config import config as default_config
            from src.logger_config import logger as default_logger
        
        self.config = config_instance or default_config
        self.logger = default_logger
        self.collector = RoboticsDataCollector(self.config)
        self.analyzer = RoboticsProjectionAnalyzer(self.config)
        self.output_dir = self.config.FIGURES_DIR
        
        # Load data
        self.logger.info("Loading data for dashboard")
        self.global_df, self.regional_df, self.installations_df = self.collector.load_data()
        self.projections = self.analyzer.generate_2026_projections()
        
        # Use color scheme from config
        self.colors = self.config.COLORS
    
    def create_kpi_cards(self):
        """Create KPI indicator cards."""
        global_proj = self.projections['global_market_size']['ensemble']
        china_proj = self.projections['china']['ensemble']
        china_share = (china_proj / global_proj * 100) if global_proj > 0 else 0
        
        # Calculate growth rate
        last_value = self.global_df['global_market_size'].iloc[-1]
        growth_rate = ((global_proj - last_value) / last_value * 100) if last_value > 0 else 0
        
        # Calculate CAGR
        first_value = self.global_df['global_market_size'].iloc[0]
        years = len(self.global_df) - 1
        cagr = (((global_proj / first_value) ** (1 / (years + 2))) - 1) * 100
        
        return {
            'global_market': global_proj,
            'china_market': china_proj,
            'china_share': china_share,
            'growth_rate': growth_rate,
            'cagr': cagr
        }
    
    def create_comprehensive_dashboard(self):
        """Create comprehensive interactive dashboard."""
        kpis = self.create_kpi_cards()
        
        # Create subplots with custom layout
        fig = make_subplots(
            rows=4, cols=3,
            subplot_titles=(
                'Global Market Size Trend (2015-2026)', 'Regional Market Share 2026', 'Industry Segments 2026',
                'Regional Market Comparison', 'China Market Growth', 'Global vs China Installations',
                'Market Growth Rates by Region', 'Segment Growth Trends', 'Forecast Uncertainty Analysis'
            ),
            specs=[
                [{"type": "scatter", "colspan": 2}, None, {"type": "pie"}],
                [{"type": "bar"}, {"type": "scatter"}, {"type": "scatter"}],
                [{"type": "bar"}, {"type": "scatter"}, {"type": "bar"}],
                [{"type": "scatter", "colspan": 3}, None, None]
            ],
            vertical_spacing=0.08,
            horizontal_spacing=0.08
        )
        
        # 1. Global Market Trend (Row 1, Col 1-2)
        years_hist = self.global_df['year'].tolist()
        years_proj = years_hist + [2026]
        values_hist = self.global_df['global_market_size'].tolist()
        values_proj = values_hist + [self.projections['global_market_size']['ensemble']]
        
        fig.add_trace(
            go.Scatter(
                x=years_hist, y=values_hist,
                mode='lines+markers',
                name='Historical',
                line=dict(color=self.colors['primary'], width=3),
                marker=dict(size=8),
                hovertemplate='<b>%{x}</b><br>Market Size: $%{y:.1f}B<extra></extra>'
            ),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Scatter(
                x=[2024, 2026], y=[values_hist[-1], values_proj[-1]],
                mode='lines+markers',
                name='Projection',
                line=dict(color=self.colors['secondary'], width=3, dash='dash'),
                marker=dict(size=12, symbol='star'),
                hovertemplate='<b>%{x}</b><br>Projected: $%{y:.1f}B<extra></extra>'
            ),
            row=1, col=1
        )
        
        # Add confidence interval
        std_dev = self.projections['global_market_size']['std']
        upper_bound = values_proj[-1] + std_dev
        lower_bound = max(0, values_proj[-1] - std_dev)
        
        fig.add_trace(
            go.Scatter(
                x=[2026, 2026], y=[lower_bound, upper_bound],
                mode='lines',
                name='Uncertainty Range',
                line=dict(width=0),
                showlegend=False,
                hoverinfo='skip'
            ),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Scatter(
                x=[2026, 2026, None, 2026, 2026],
                y=[lower_bound, upper_bound, None, lower_bound, upper_bound],
                fill='toself',
                fillcolor='rgba(162, 59, 114, 0.2)',
                line=dict(color='rgba(255,255,255,0)'),
                name='95% Confidence',
                showlegend=True,
                hovertemplate='Range: $%{y:.1f}B<extra></extra>'
            ),
            row=1, col=1
        )
        
        # 2. Regional Market Share Pie (Row 1, Col 3)
        regions = ['china', 'usa', 'japan', 'germany', 'south_korea', 'rest_of_world']
        region_names = ['China', 'USA', 'Japan', 'Germany', 'South Korea', 'Rest of World']
        region_values = [self.projections[r]['ensemble'] for r in regions]
        region_colors = [self.colors['china'], self.colors['usa'], self.colors['japan'],
                        self.colors['germany'], self.colors['south_korea'], self.colors['primary']]
        
        fig.add_trace(
            go.Pie(
                labels=region_names,
                values=region_values,
                marker=dict(colors=region_colors),
                textinfo='label+percent',
                texttemplate='%{label}<br>%{percent}<br>$%{value:.1f}B',
                hovertemplate='<b>%{label}</b><br>Value: $%{value:.1f}B<br>Share: %{percent}<extra></extra>',
                hole=0.4
            ),
            row=1, col=3
        )
        
        # 3. Industry Segments Bar (Row 2, Col 1)
        segments = {
            'industrial_robots': 'Industrial',
            'service_robots': 'Service',
            'medical_robots': 'Medical',
            'agricultural_robots': 'Agricultural'
        }
        segment_names = list(segments.values())
        segment_values = [self.projections[s]['ensemble'] for s in segments.keys()]
        segment_colors = [self.colors['primary'], self.colors['accent'], 
                         self.colors['success'], self.colors['warning']]
        
        fig.add_trace(
            go.Bar(
                x=segment_names,
                y=segment_values,
                marker=dict(color=segment_colors),
                text=[f'${v:.1f}B' for v in segment_values],
                textposition='outside',
                hovertemplate='<b>%{x}</b><br>Market Size: $%{y:.1f}B<extra></extra>'
            ),
            row=2, col=1
        )
        
        # 4. Regional Comparison Bar (Row 2, Col 2)
        fig.add_trace(
            go.Bar(
                x=region_names,
                y=region_values,
                marker=dict(color=region_colors),
                text=[f'${v:.1f}B' for v in region_values],
                textposition='outside',
                hovertemplate='<b>%{x}</b><br>Market Size: $%{y:.1f}B<extra></extra>'
            ),
            row=2, col=2
        )
        
        # 5. China Market Growth (Row 2, Col 3)
        china_years = self.regional_df['year'].tolist() + [2026]
        china_values = self.regional_df['china'].tolist() + [self.projections['china']['ensemble']]
        
        fig.add_trace(
            go.Scatter(
                x=self.regional_df['year'], y=self.regional_df['china'],
                mode='lines+markers',
                name='China Historical',
                line=dict(color=self.colors['china'], width=3),
                hovertemplate='<b>%{x}</b><br>China: $%{y:.1f}B<extra></extra>'
            ),
            row=2, col=3
        )
        
        fig.add_trace(
            go.Scatter(
                x=[2024, 2026], y=[china_values[-2], china_values[-1]],
                mode='lines+markers',
                name='China Projection',
                line=dict(color=self.colors['china'], width=3, dash='dash'),
                marker=dict(size=10, symbol='star'),
                hovertemplate='<b>%{x}</b><br>Projected: $%{y:.1f}B<extra></extra>'
            ),
            row=2, col=3
        )
        
        # 6. Global vs China Installations (Row 3, Col 1)
        global_inst_years = self.installations_df['year'].tolist() + [2026]
        global_inst = self.installations_df['global_installations'].tolist() + [
            self.projections['global_installations']['ensemble']
        ]
        china_inst = self.installations_df['china_installations'].tolist() + [
            self.projections['china_installations']['ensemble']
        ]
        
        fig.add_trace(
            go.Scatter(
                x=self.installations_df['year'], y=self.installations_df['global_installations'],
                mode='lines+markers',
                name='Global Installations',
                line=dict(color=self.colors['primary'], width=2),
                hovertemplate='<b>%{x}</b><br>Global: %{y:.0f}k units<extra></extra>'
            ),
            row=3, col=1
        )
        
        fig.add_trace(
            go.Scatter(
                x=self.installations_df['year'], y=self.installations_df['china_installations'],
                mode='lines+markers',
                name='China Installations',
                line=dict(color=self.colors['china'], width=2),
                hovertemplate='<b>%{x}</b><br>China: %{y:.0f}k units<extra></extra>'
            ),
            row=3, col=1
        )
        
        # 7. Growth Rates by Region (Row 3, Col 2)
        growth_rates = []
        for region in regions:
            hist_values = self.regional_df[region].values
            proj_value = self.projections[region]['ensemble']
            growth = ((proj_value - hist_values[-1]) / hist_values[-1] * 100) if hist_values[-1] > 0 else 0
            growth_rates.append(growth)
        
        fig.add_trace(
            go.Bar(
                x=region_names,
                y=growth_rates,
                marker=dict(color=region_colors),
                text=[f'{g:.1f}%' for g in growth_rates],
                textposition='outside',
                hovertemplate='<b>%{x}</b><br>Growth: %{y:.1f}%<extra></extra>'
            ),
            row=3, col=2
        )
        
        # 8. Segment Growth Trends (Row 3, Col 3)
        for seg_key, seg_name in segments.items():
            seg_values = self.global_df[seg_key].tolist() + [self.projections[seg_key]['ensemble']]
            seg_years = self.global_df['year'].tolist() + [2026]
            
            fig.add_trace(
                go.Scatter(
                    x=seg_years, y=seg_values,
                    mode='lines+markers',
                    name=seg_name,
                    line=dict(width=2),
                    hovertemplate=f'<b>{seg_name}</b><br>%{{x}}: $%{{y:.1f}}B<extra></extra>',
                    showlegend=False
                ),
                row=3, col=3
            )
        
        # 9. Forecast Uncertainty Analysis (Row 4, Col 1-3)
        metrics = ['Global Market', 'China', 'Industrial', 'Service', 'Medical', 'Agricultural']
        metric_keys = ['global_market_size', 'china', 'industrial_robots', 
                      'service_robots', 'medical_robots', 'agricultural_robots']
        
        ensemble_values = [self.projections[k]['ensemble'] for k in metric_keys]
        std_values = [self.projections[k]['std'] for k in metric_keys]
        lower_bounds = [e - s for e, s in zip(ensemble_values, std_values)]
        upper_bounds = [e + s for e, s in zip(ensemble_values, std_values)]
        
        fig.add_trace(
            go.Scatter(
                x=metrics, y=ensemble_values,
                mode='markers+lines',
                name='Ensemble Forecast',
                line=dict(color=self.colors['primary'], width=2),
                marker=dict(size=10, color=self.colors['primary']),
                hovertemplate='<b>%{x}</b><br>Forecast: $%{y:.1f}B<extra></extra>'
            ),
            row=4, col=1
        )
        
        for i, (metric, lower, upper) in enumerate(zip(metrics, lower_bounds, upper_bounds)):
            fig.add_trace(
                go.Scatter(
                    x=[metric, metric], y=[lower, upper],
                    mode='lines',
                    line=dict(color=self.colors['secondary'], width=4),
                    showlegend=(i == 0),
                    name='Uncertainty Range',
                    hovertemplate='Range: $%{y:.1f}B<extra></extra>'
                ),
                row=4, col=1
            )
        
        # Update layout
        fig.update_layout(
            height=1600,
            title=dict(
                text='<b>Robotics Industry Projections 2026 - Comprehensive Dashboard</b><br>' +
                     f'<span style="font-size:14px">Generated: {datetime.now().strftime("%Y-%m-%d %H:%M")}</span>',
                x=0.5,
                xanchor='center',
                font=dict(size=20, color='#1f1f1f')
            ),
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            hovermode='closest',
            template='plotly_white',
            paper_bgcolor='white',
            plot_bgcolor='rgba(240,240,240,0.5)'
        )
        
        # Update axes
        fig.update_xaxes(title_text="Year", row=1, col=1)
        fig.update_yaxes(title_text="Market Size (Billion USD)", row=1, col=1)
        fig.update_yaxes(title_text="Market Size (Billion USD)", row=2, col=1)
        fig.update_xaxes(title_text="Region", row=2, col=2)
        fig.update_yaxes(title_text="Market Size (Billion USD)", row=2, col=2)
        fig.update_xaxes(title_text="Year", row=2, col=3)
        fig.update_yaxes(title_text="Market Size (Billion USD)", row=2, col=3)
        fig.update_xaxes(title_text="Year", row=3, col=1)
        fig.update_yaxes(title_text="Installations (Thousand Units)", row=3, col=1)
        fig.update_xaxes(title_text="Region", row=3, col=2)
        fig.update_yaxes(title_text="Growth Rate (%)", row=3, col=2)
        fig.update_xaxes(title_text="Year", row=3, col=3)
        fig.update_yaxes(title_text="Market Size (Billion USD)", row=3, col=3)
        fig.update_xaxes(title_text="Metric", row=4, col=1)
        fig.update_yaxes(title_text="Market Size (Billion USD)", row=4, col=1)
        
        return fig
    
    def create_executive_summary_dashboard(self):
        """Create a clean executive summary dashboard with KPIs."""
        kpis = self.create_kpi_cards()
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=(
                'Global Market Growth (2015-2026)',
                'Regional Market Distribution',
                'Industry Segment Analysis',
                'China Market Position'
            ),
            specs=[
                [{"type": "scatter"}, {"type": "pie"}],
                [{"type": "bar"}, {"type": "scatter"}]
            ],
            vertical_spacing=0.15,
            horizontal_spacing=0.15
        )
        
        # 1. Global Market Growth
        years = self.global_df['year'].tolist() + [2026]
        values = self.global_df['global_market_size'].tolist() + [
            self.projections['global_market_size']['ensemble']
        ]
        
        fig.add_trace(
            go.Scatter(
                x=years[:-1], y=values[:-1],
                mode='lines+markers',
                name='Historical',
                line=dict(color=self.colors['primary'], width=4),
                marker=dict(size=10),
                fill='tozeroy',
                fillcolor='rgba(46, 134, 171, 0.2)'
            ),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Scatter(
                x=[2024, 2026], y=[values[-2], values[-1]],
                mode='lines+markers',
                name='2026 Projection',
                line=dict(color=self.colors['secondary'], width=4, dash='dash'),
                marker=dict(size=15, symbol='star')
            ),
            row=1, col=1
        )
        
        # 2. Regional Distribution
        regions = ['china', 'usa', 'japan', 'germany', 'south_korea', 'rest_of_world']
        region_names = ['China', 'USA', 'Japan', 'Germany', 'South Korea', 'Rest of World']
        region_values = [self.projections[r]['ensemble'] for r in regions]
        region_colors = [self.colors['china'], self.colors['usa'], self.colors['japan'],
                        self.colors['germany'], self.colors['south_korea'], self.colors['primary']]
        
        fig.add_trace(
            go.Pie(
                labels=region_names,
                values=region_values,
                marker=dict(colors=region_colors),
                textinfo='label+percent+value',
                texttemplate='%{label}<br>$%{value:.1f}B'
            ),
            row=1, col=2
        )
        
        # 3. Segment Analysis
        segments = {
            'industrial_robots': 'Industrial',
            'service_robots': 'Service',
            'medical_robots': 'Medical',
            'agricultural_robots': 'Agricultural'
        }
        segment_names = list(segments.values())
        segment_values = [self.projections[s]['ensemble'] for s in segments.keys()]
        
        fig.add_trace(
            go.Bar(
                x=segment_names,
                y=segment_values,
                marker=dict(color=[self.colors['primary'], self.colors['accent'],
                                 self.colors['success'], self.colors['warning']]),
                text=[f'${v:.1f}B' for v in segment_values],
                textposition='outside'
            ),
            row=2, col=1
        )
        
        # 4. China Market Position
        china_years = self.regional_df['year'].tolist() + [2026]
        china_values = self.regional_df['china'].tolist() + [
            self.projections['china']['ensemble']
        ]
        usa_values = self.regional_df['usa'].tolist() + [
            self.projections['usa']['ensemble']
        ]
        
        fig.add_trace(
            go.Scatter(
                x=china_years, y=china_values,
                mode='lines+markers',
                name='China',
                line=dict(color=self.colors['china'], width=4),
                marker=dict(size=10)
            ),
            row=2, col=2
        )
        
        fig.add_trace(
            go.Scatter(
                x=china_years, y=usa_values,
                mode='lines+markers',
                name='USA',
                line=dict(color=self.colors['usa'], width=4),
                marker=dict(size=10)
            ),
            row=2, col=2
        )
        
        # Update layout
        fig.update_layout(
            height=900,
            title=dict(
                text=f'<b>Robotics Industry 2026: ${kpis["global_market"]:.1f}B Global Market</b><br>' +
                     f'<span style="font-size:14px">China: ${kpis["china_market"]:.1f}B ({kpis["china_share"]:.1f}% share) | ' +
                     f'CAGR: {kpis["cagr"]:.1f}%</span>',
                x=0.5,
                xanchor='center',
                font=dict(size=18)
            ),
            showlegend=True,
            template='plotly_white'
        )
        
        # Update axes
        fig.update_xaxes(title_text="Year", row=1, col=1)
        fig.update_yaxes(title_text="Market Size (Billion USD)", row=1, col=1)
        fig.update_xaxes(title_text="Segment", row=2, col=1)
        fig.update_yaxes(title_text="Market Size (Billion USD)", row=2, col=1)
        fig.update_xaxes(title_text="Year", row=2, col=2)
        fig.update_yaxes(title_text="Market Size (Billion USD)", row=2, col=2)
        
        return fig
    
    def save_dashboard(self, dashboard_type='comprehensive'):
        """Save dashboard to HTML file."""
        if dashboard_type == 'comprehensive':
            fig = self.create_comprehensive_dashboard()
            filename = 'robotics_dashboard_comprehensive.html'
        else:
            fig = self.create_executive_summary_dashboard()
            filename = 'robotics_dashboard_executive.html'
        
        output_path = self.config.get_figure_path(filename)
        fig.write_html(str(output_path), config={'displayModeBar': True})
        self.logger.info(f"Dashboard saved: {output_path}")
        print(f"Dashboard saved: {output_path}")
        return output_path


if __name__ == "__main__":
    dashboard = RoboticsDashboard()
    print("Creating comprehensive dashboard...")
    dashboard.save_dashboard('comprehensive')
    print("\nCreating executive summary dashboard...")
    dashboard.save_dashboard('executive')
    print("\nDashboards created successfully!")

