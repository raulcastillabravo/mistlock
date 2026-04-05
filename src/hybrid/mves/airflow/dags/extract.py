import pandas as pd
import numpy as np
from datetime import datetime
import os

class Extract:
    def __init__(self):
        self.output_dir = "storage/extract"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def run(self):
        """
        Extracts data by creating a DataFrame with random values
        Writes it to a CSV file and returns the file path
        """
        print("Starting data extraction...")
        
        # Generate random data
        data = {
            'id': range(1, 6),
            'value': np.random.randint(1, 100, size=5),
            'category': np.random.choice(['A', 'B', 'C'], size=5)
        }
        
        df = pd.DataFrame(data)
        
        # Generate timestamp and file path
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = os.path.join(self.output_dir, f"data_{timestamp}.csv")
        
        # Write to CSV
        df.to_csv(file_path, index=False)
        
        print(f"✓ Extracted {len(df)} rows")
        print(f"✓ Saved to: {file_path}")
        print(f"\nExtracted data:\n{df}")
        
        return file_path

if __name__ == "__main__":
    extractor = Extract()
    extractor.run()