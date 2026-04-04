import pandas as pd
import os
from minio_client import MinioClient

BUCKET_NAME = os.getenv("BUCKET_NAME", "test-bucket")
FILE_NAME = "data.csv"
DOWNLOADED_FILE_NAME = "downloaded_data.csv"

def main():
    client = MinioClient()

    # Create a dummy DataFrame
    df = pd.DataFrame({
        'id': range(1, 6),
        'value': [x * 10 for x in range(1, 6)],
        'category': ['A', 'B', 'A', 'B', 'C']
    })
    print("Created dummy DataFrame:")
    print(df)

    # Save DataFrame to CSV
    df.to_csv(FILE_NAME, index=False)
    print(f"Saved DataFrame to '{FILE_NAME}'.")

    # Upload File
    client.upload_file(FILE_NAME, BUCKET_NAME)

    # Download File
    client.download_file(BUCKET_NAME, FILE_NAME, DOWNLOADED_FILE_NAME)

    # Verify Download
    if os.path.exists(DOWNLOADED_FILE_NAME):
        downloaded_df = pd.read_csv(DOWNLOADED_FILE_NAME)
        print("Downloaded DataFrame:")
        print(downloaded_df)
    
    # Clean up local files only
    if os.path.exists(FILE_NAME):
        os.remove(FILE_NAME)
    if os.path.exists(DOWNLOADED_FILE_NAME):
        os.remove(DOWNLOADED_FILE_NAME)
    print("Local files cleaned up.")

if __name__ == "__main__":
    main()
