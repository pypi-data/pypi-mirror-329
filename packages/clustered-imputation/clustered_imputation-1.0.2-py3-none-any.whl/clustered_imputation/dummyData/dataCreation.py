import pandas as pd
import numpy as np

# Define categories
categories1 = ['A', 'B', 'C']
categories2 = ['X', 'Y', 'Z']
categories3 = ['Red', 'Green', 'Blue']

# Create DataFrame
np.random.seed(42)
data = pd.DataFrame({
    'Cat1': np.random.choice(categories1, 20),
    'Cat2': np.random.choice(categories2, 20),
    'Cat3': np.random.choice(categories3, 20),
    'Num1': np.random.randint(10, 100, 20),
    'Num2': np.random.uniform(1.0, 50.0, 20),
    'Num3': np.random.randint(200, 500, 20)
})

# Introduce missing values
for col in data.columns:
    data.loc[np.random.choice(data.index, size=5, replace=False), col] = np.nan
