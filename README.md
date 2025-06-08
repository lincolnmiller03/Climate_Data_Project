# Climate Data Analysis Project

## Overview  
This project analyzes precipitation trends (2013-2023) for four Midwestern US cities: Chicago, Madison, Minneapolis, and St. Louis. The code provides tools to:  
1. Combine climate data from multiple city-specific CSV files  
2. Visualize monthly precipitation trends  
3. Compare precipitation between years (2013 vs. 2023)  
4. Perform statistical analysis of precipitation differences  

## Requirements  
- Python 3.7+  
- Required packages:  
  - pandas  
  - numpy  
  - matplotlib  
  - seaborn  
  - scipy  

## Data Preparation

Place your city climate data CSV files in the same directory as the script with the following names:

chicago.csv
madison.csv
minneapolis.csv
st_louis.csv
Functions

## Functions
### combine_city_climate_data()

Combines climate data from all four cities into a single DataFrame.

Returns:

- A pandas DataFrame with all city data and a 'CITY' identifier column
- None if any file fails to load

### plot_monthly_precipitation_trends(df, output_path, figsize, dpi, linewidth)

Generates a line plot showing monthly precipitation trends across all cities.

Parameters:

- df: Combined city data DataFrame
- output_path: Optional path to save figure (default: shows plot interactively)
- figsize: Figure dimensions (default: (12,6))
- dpi: Image resolution (default: 300)
- linewidth: Trend line width (default: 2.5)

### plot_yearly_comparison(df, year1, year2, output_path, figsize, dpi)

Creates a 2×2 grid of plots comparing monthly precipitation between two years.

Parameters:

- df: Combined city data DataFrame
- year1: First comparison year (default: 2013)
- year2: Second comparison year (default: 2023)
- output_path: Optional path to save figure
- figsize: Figure dimensions (default: (18,12))
- dpi: Image resolution (default: 300)

### compare_precipitation_stats(df, alpha)

Performs statistical comparison of precipitation between 2013 and 2023.

Parameters:

- df: Combined city data DataFrame
- alpha: Significance level (default: 0.1)

Returns:

DataFrame with test results including p-values and effect sizes
