import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
from typing import Optional
from scipy import stats

from climate_data import *


# Don't use absolute paths, they only work for you.
city_files = {
    'Chicago':     'data/chicago.csv',            # CHICAGO DATA HERE
    'Madison':     'data/madison.csv',            # MADISON DATA HERE
    'Minneapolis': 'data/minneapolis.csv',    # MINNEAPOLIS DATA HERE
    'St. Louis':   'data/st_louis.csv'          # ST. LOUIS DATA HERE
}


cities = combine_city_climate_data(city_files)

plot_monthly_precipitation_trends(cities)