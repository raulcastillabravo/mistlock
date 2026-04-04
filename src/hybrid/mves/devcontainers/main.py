import os

import pandas as pd
from dotenv import load_dotenv

load_dotenv()

# Load environment variable
EXAMPLE_VAR = os.getenv("EXAMPLE_VAR", "default-value")

def main():
    print(f"Environment variable EXAMPLE_VAR: {EXAMPLE_VAR}\n")
    print("Creating a pandas DataFrame...")
    
    # Create a simple DataFrame
    data = {
        'Name': ['Alice', 'Bob', 'Charlie', 'Diana'],
        'Age': [25, 30, 35, 28],
        'City': ['New York', 'San Francisco', 'Los Angeles', 'Chicago']
    }
    
    df = pd.DataFrame(data)
    
    print("\nDataFrame created successfully!")
    print("\nDataFrame contents:")
    print(df)
    
    print("\nDataFrame info:")
    print(df.info())
    
    print("\nDataFrame statistics:")
    print(df.describe())

if __name__ == "__main__":
    main()

