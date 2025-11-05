# Quick Start Guide

## Installation (One-Time Setup)

1. **Install Python 3.8+** (if not already installed)
   - Download from https://www.python.org/downloads/

2. **Create Virtual Environment** (recommended)
   ```powershell
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```powershell
   pip install -r requirements.txt
   ```

## Running the Analysis

### Option 1: Windows Batch Script (Easiest)
```powershell
RUN_ANALYSIS.bat
```

### Option 2: Python Script
```powershell
python src\run_analysis.py
```

### Option 3: Jupyter Notebook
```powershell
jupyter notebook notebooks\example_analysis.ipynb
```

## What You'll Get

After running the analysis, check these outputs:

1. **Projections CSV**: `data\processed\projections_2026.csv`
2. **Report**: `outputs\reports\projection_report_2026.txt`
3. **Visualizations**: `outputs\figures\`
   - Global market trend chart
   - Regional comparison
   - Segment breakdown
   - China market analysis (interactive HTML)

## Key Files

- `src\data_collection.py` - Data handling
- `src\analysis.py` - Projection calculations
- `src\visualization.py` - Chart generation
- `src\run_analysis.py` - Main script
- `docs\METHODOLOGY.md` - Detailed methodology
- `docs\PROJECT_SUMMARY.md` - Project overview

## Troubleshooting

**Import Errors**: Make sure you're running from the project root directory

**Missing Dependencies**: Run `pip install -r requirements.txt`

**Directory Errors**: The scripts create directories automatically, but ensure you have write permissions

## Next Steps

1. Review the generated report
2. Explore visualizations
3. Modify parameters in `src\analysis.py` for different scenarios
4. Add your own data sources to `src\data_collection.py`

