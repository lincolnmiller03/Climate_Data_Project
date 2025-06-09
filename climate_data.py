
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def combine_city_climate_data(city_files):
        
        combined_data = []
        
        for city, file_path in city_files.items():

            # Read the city's data
            df = pd.read_csv(file_path, parse_dates=['DATE'],)
            
            # Add city identifier column
            df['CITY'] = city
            
            # Ensure consistent column names (handling potential duplicates like 'DailyPrecipitation.1')
            df.columns = df.columns.str.replace('.1', '_dup', regex=False)
            
            combined_data.append(df)
            #print(f"Successfully loaded data for {city}")
                
            
        
        # Combine all city data
        df = pd.concat(combined_data, axis=0, ignore_index=True)
        
        # Clean up any duplicate columns
        df = df.loc[:,~df.columns.duplicated()]
        

        
        df['DailyPrecipitation'] = pd.to_numeric(df['DailyPrecipitation'], errors='coerce')
        df['Month'] = df['DATE'].dt.month_name()
        df['Year'] = df['DATE'].dt.year

        #print("Successfully combined all city data!")
        return df


def plot_monthly_precipitation_trends(
        df: pd.DataFrame,
        output_path: Optional[str] = None,
        figsize: tuple = (12, 6),
        dpi: int = 300,
        linewidth: float = 2.5
    ) -> None:
    # Data preparation

    # Making a copy of a dataframe can be expensive.
    X = df.dropna(subset=['DailyPrecipitation'])
    
    # Calculate monthly averages
    monthly_avg = (
        X
        .groupby(['CITY', 'Month'])['DailyPrecipitation']
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