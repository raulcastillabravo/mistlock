import pandas as pd
import os
import shutil

class Load:
    def __init__(self):
        self.output_dir = "storage/load"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def run(self, input_path: str):
        """
        Loads data by copying the transformed CSV to the load directory
        Returns the number of rows loaded
        """
        print(f"Starting data loading...")
        print(f"Reading from: {input_path}")
        
        # Read input CSV
        df = pd.read_csv(input_path)
        
        print(f"\nData to be loaded:\n{df}")
        
        # Generate output file path with same timestamp
        file_name = os.path.basename(input_path)
        output_path = os.path.join(self.output_dir, file_name)
        
        # Write to CSV (simulating database insert)
        df.to_csv(output_path, index=False)
        
        num_rows = len(df)
        print(f"\n✓ Inserted {num_rows} rows into database")
        print(f"✓ Saved to: {output_path}")
        
        return num_rows

if __name__ == "__main__":
    # For testing purposes
    loader = Load()
    # Assumes there's a file in storage/transform/
    test_file = "storage/transform/data_test.csv"
    if os.path.exists(test_file):
        loader.run(test_file)