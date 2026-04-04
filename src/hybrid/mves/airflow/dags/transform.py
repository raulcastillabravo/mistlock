import pandas as pd
import os

class Transform:
    def __init__(self):
        self.output_dir = "storage/transform"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def run(self, input_path: str):
        """
        Transforms data by doubling the 'value' column
        Writes transformed data to a new CSV file and returns the file path
        """
        print(f"Starting data transformation...")
        print(f"Reading from: {input_path}")
        
        # Read input CSV
        df = pd.read_csv(input_path)
        
        print(f"\nData before transformation:\n{df}")
        
        # Simple transformation: double the value column
        df['value'] = df['value'] * 2
        
        # Generate output file path with same timestamp
        file_name = os.path.basename(input_path)
        output_path = os.path.join(self.output_dir, file_name)
        
        # Write to CSV
        df.to_csv(output_path, index=False)
        
        print(f"\n✓ Transformed {len(df)} rows")
        print(f"✓ Saved to: {output_path}")
        print(f"\nData after transformation:\n{df}")
        
        return output_path

if __name__ == "__main__":
    # For testing purposes
    transformer = Transform()
    # Assumes there's a file in storage/extract/
    test_file = "storage/extract/data_test.csv"
    if os.path.exists(test_file):
        transformer.run(test_file)