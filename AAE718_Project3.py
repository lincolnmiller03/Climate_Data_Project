# AAE 718 - Project 3
# Lincoln Miller

if __name__ == "__main__":

    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns
    import numpy as np
    import os
    from typing import Optional
    from scipy import stats
    
    def combine_city_climate_data():
        city_files = {
            'Chicago': '/Users/lincolnmiller/Desktop/AAE 718/Project 3/chicago.csv',            # CHICAGO DATA HERE
            'Madison': '/Users/lincolnmiller/Desktop/AAE 718/Project 3/madison.csv',            # MADISON DATA HERE
            'Minneapolis': '/Users/lincolnmiller/Desktop/AAE 718/Project 3/minneapolis.csv',    # MINNEAPOLIS DATA HERE
            'St. Louis': '/Users/lincolnmiller/Desktop/AAE 718/Project 3/st_louis.csv'          # ST. LOUIS DATA HERE
        }
        
        combined_data = []
        
        for city, file_path in city_files.items():
            try:
                # Read the city's data
                df = pd.read_csv(file_path)
                
                # Add city identifier column
                df['CITY'] = city
                
                # Ensure consistent column names (handling potential duplicates like 'DailyPrecipitation.1')
                df.columns = df.columns.str.replace('.1', '_dup', regex=False)
                
                combined_data.append(df)
                print(f"Successfully loaded data for {city}")
                
            except FileNotFoundError:
                print(f"Error: File not found for {city} at {file_path}")
                return None
            except Exception as e:
                print(f"Error loading {city} data: {str(e)}")
                return None
        
        # Combine all city data
        final_df = pd.concat(combined_data, axis=0, ignore_index=True)
        
        # Clean up any duplicate columns
        final_df = final_df.loc[:,~final_df.columns.duplicated()]
        
        print("Successfully combined all city data!")
        return final_df

    cities = combine_city_climate_data()
    cities
    def plot_monthly_precipitation_trends(
        df: pd.DataFrame,
        output_path: Optional[str] = None,
        figsize: tuple = (12, 6),
        dpi: int = 300,
        linewidth: float = 2.5
    ) -> None:
        # Data preparation
        df = df.copy()
        df['DATE'] = pd.to_datetime(df['DATE'])
        df['DailyPrecipitation'] = pd.to_numeric(df['DailyPrecipitation'], errors='coerce')
        df['Month'] = df['DATE'].dt.month_name()
        df['Year'] = df['DATE'].dt.year
        df = df.dropna(subset=['DailyPrecipitation'])
        
        # Calculate monthly averages
        monthly_avg = (
            df.groupby(['CITY', 'Month'])['DailyPrecipitation']
            .mean()
            .reset_index()
            .sort_values('Month', key=lambda x: pd.to_datetime(x, format='%B').dt.month)
        )
        
        # Create plot
        plt.figure(figsize=figsize)
        sns.set_style("whitegrid")
        
        ax = sns.lineplot(
            data=monthly_avg,
            x='Month', y='DailyPrecipitation',
            hue='CITY',
            marker='o',
            sort=False,
            linewidth=linewidth
        )
        
        # Formatting
        plt.title("Monthly Precipitation Trends (2013-2023)")
        plt.ylabel("Avg Precipitation (inches)")
        plt.xlabel("")
        plt.xticks(rotation=45)
        plt.grid(alpha=0.3)
        plt.legend(title="City")
        plt.tight_layout()
        
        # Output handling
        if output_path:
            plt.savefig(output_path, dpi=dpi, bbox_inches='tight')
            print(f"Figure saved to {output_path}")
            plt.close()
        else:
            plt.show()

    plot_monthly_precipitation_trends(cities, output_path="precip_trends.png")
    def plot_yearly_comparison(
        df: pd.DataFrame,
        year1: int = 2013,
        year2: int = 2023,
        output_path: str = None,
        figsize: tuple = (18, 12),
        dpi: int = 300
    ) -> None:
        
        # Data preparation
        df = df.copy()
        df['DATE'] = pd.to_datetime(df['DATE'])
        df['DailyPrecipitation'] = pd.to_numeric(df['DailyPrecipitation'], errors='coerce')
        df['Month'] = df['DATE'].dt.month_name()
        df['Year'] = df['DATE'].dt.year
        df = df.dropna(subset=['DailyPrecipitation'])
        
        # Filter for target years
        df = df[df['Year'].isin([year1, year2])]
        
        # Calculate monthly and yearly averages
        monthly_avg = (
            df.groupby(['CITY', 'Year', 'Month'])['DailyPrecipitation']
            .mean()
            .reset_index()
            .sort_values(['Year', 'Month'], 
                        key=lambda x: pd.to_datetime(x, format='%B').dt.month if x.name == 'Month' else x)
        )
        
        yearly_avg = df.groupby(['CITY', 'Year'])['DailyPrecipitation'].mean().reset_index()
        
        # City styling
        city_colors = {
            'Chicago': 'blue',
            'Madison': 'orange',
            'Minneapolis': 'green',
            'St. Louis': 'red'
        }
        month_order = ['January', 'February', 'March', 'April', 'May', 'June',
                    'July', 'August', 'September', 'October', 'November', 'December']
        
        # Create plot
        plt.figure(figsize=figsize)
        sns.set_style("whitegrid")
        plt.suptitle(f"Monthly Precipitation Comparison: {year1} vs. {year2}\n(Dashed Horizontal Lines Show Yearly Averages)", 
                    y=1.02, fontsize=16)
        
        for i, city in enumerate(city_colors.keys(), 1):
            ax = plt.subplot(2, 2, i)
            city_data = monthly_avg[monthly_avg['CITY'] == city]
            
            # Get yearly averages
            city_yr_avg = yearly_avg[yearly_avg['CITY'] == city]
            avg_y1 = city_yr_avg[city_yr_avg['Year'] == year1]['DailyPrecipitation'].values[0]
            avg_y2 = city_yr_avg[city_yr_avg['Year'] == year2]['DailyPrecipitation'].values[0]
            
            # Plot monthly data
            sns.lineplot(data=city_data[city_data['Year'] == year1], 
                        x='Month', y='DailyPrecipitation',
                        color=city_colors[city], linestyle='--', marker='o', 
                        label=str(year1), sort=False, ax=ax)
            
            sns.lineplot(data=city_data[city_data['Year'] == year2], 
                        x='Month', y='DailyPrecipitation',
                        color=city_colors[city], linestyle='-', marker='o', 
                        label=str(year2), sort=False, ax=ax)
            
            # Add reference lines
            ax.axhline(avg_y1, color=city_colors[city], linestyle=':', alpha=0.5,
                    label=f'{year1} Avg: {avg_y1:.2f}"')
            ax.axhline(avg_y2, color=city_colors[city], linestyle='-.', alpha=0.5,
                    label=f'{year2} Avg: {avg_y2:.2f}"')
            
            # Formatting
            ax.set_title(city, fontweight='bold')
            ax.set_xticklabels([m[:3] for m in month_order], rotation=45)
            ax.set_ylabel("Precipitation (inches)")
            ax.set_xlabel("")
            ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
            ax.grid(alpha=0.3)
        
        plt.tight_layout()
        
        if output_path:
            plt.savefig(output_path, dpi=dpi, bbox_inches='tight')
            plt.close()
            print(f"Figure saved to {output_path}")
        else:
            plt.show()

    plot_yearly_comparison(cities, output_path="precip_comparison.png")
    def compare_precipitation_stats(df: pd.DataFrame, alpha: float = 0.1) -> pd.DataFrame:
        # Data preparation
        df = df.copy()
        df['DATE'] = pd.to_datetime(df['DATE'])
        df['Year'] = df['DATE'].dt.year
        df['DailyPrecipitation'] = pd.to_numeric(df['DailyPrecipitation'], errors='coerce')
        df = df.dropna(subset=['DailyPrecipitation'])
        
        # Filter for target years
        df = df[df['Year'].isin([2013, 2023])]
        
        # Initialize results storage
        results = []
        
        # Test for each city
        for city in df['CITY'].unique():
            # Extract data
            y2013 = df[(df['CITY'] == city) & (df['Year'] == 2013)]['DailyPrecipitation']
            y2023 = df[(df['CITY'] == city) & (df['Year'] == 2023)]['DailyPrecipitation']
            
            # Independent t-test (Welch's)
            t_stat, p_val = stats.ttest_ind(y2013, y2023, equal_var=False, nan_policy='omit')
            
            # Calculate effect size (Cohen's d)
            pooled_std = np.sqrt((y2013.std()**2 + y2023.std()**2)/2)
            cohens_d = (y2023.mean() - y2013.mean()) / pooled_std
            
            # Store results
            results.append({
                'City': city,
                '2013_Mean': y2013.mean(),
                '2023_Mean': y2023.mean(),
                'Mean_Difference': y2023.mean() - y2013.mean(),
                'p_value': p_val,
                'Significant': p_val < alpha,
                'Test_Used': "Welch's t-test",
                'Effect_Size': cohens_d
            })
        
        return pd.DataFrame(results)

    # Example usage:
    results = compare_precipitation_stats(cities)
    print(results)

    # Visualize results
    plt.figure(figsize=(10, 6))
    sns.barplot(data=results, x='City', y='Mean_Difference', 
                hue='Significant', dodge=False)
    plt.axhline(0, color='black', linestyle='--')
    plt.title("2013 vs. 2023 Precipitation Differences\n(Significant at α=0.1)")
    plt.ylabel("Difference in Mean Precipitation (inches)")
    plt.xlabel("")
    plt.savefig('precip_diff', bbox_inches='tight')
    plt.show()

    compare_precipitation_stats(cities, 0.1)