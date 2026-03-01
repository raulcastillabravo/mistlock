import os, time, csv, io
from google.cloud import storage
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()
os.environ["STORAGE_EMULATOR_HOST"] = os.getenv("FIREBASE_STORAGE_EMULATOR_HOST")

def main():
    print("🚀 Starting demo...")
    client = storage.Client(project=os.getenv("GCP_PROJECT"))
    bucket = client.create_bucket(os.getenv("STORAGE_BUCKET"))
    
    csv_data = "name,email\nAntigravity,anti@gravity.ai\nUser,user@example.com"
    blob = bucket.blob("users.csv")
    blob.upload_from_string(csv_data)
    print("✅ CSV uploaded to storage emulator.")

    engine = create_engine(os.getenv("DATABASE_URL"))
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
