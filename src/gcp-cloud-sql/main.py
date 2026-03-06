import os, time
from google.cloud import storage
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

GCP_PROJECT = os.getenv("GCP_PROJECT")
STORAGE_BUCKET = os.getenv("STORAGE_BUCKET")
DATABASE_URL = os.getenv("DATABASE_URL")

CSV_DATA = """name,email
Antigravity,anti@gravity.ai
User,user@example.com"""

def main():
    print("🚀 Starting demo...")
    client = storage.Client(project=GCP_PROJECT)
    bucket = client.bucket(STORAGE_BUCKET)
    
    blob = bucket.blob("users.csv")
    blob.upload_from_string(CSV_DATA)
    print("✅ CSV uploaded to storage emulator.")

    engine = create_engine(DATABASE_URL)
    for _ in range(10):
        try:
            with engine.connect() as conn:
                result = conn.execute(text("SELECT * FROM users")).fetchall()
                if result:
                    print(f"📊 Found {len(result)} records in Postgres:")
                    for row in result: print(f" - {row.name} ({row.email})")
                    return
        except Exception: pass
        print("⏳ Waiting for Cloud Function... (1s)")
        time.sleep(1)

if __name__ == "__main__":
    main()
