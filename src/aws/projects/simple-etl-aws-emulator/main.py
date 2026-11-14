from datetime import datetime, timezone

from dotenv import load_dotenv

from src.file_pipeline import FilePipeline


load_dotenv()


SAMPLE_FILES = [
    ("document.pdf", b"Sample PDF content", "application/pdf"),
    ("image.jpg", b"Sample image data", "image/jpeg"),
    ("data.json", b'{"status": "ok"}', "application/json"),
]


def main():
    pipeline = FilePipeline()
    since = datetime.now(timezone.utc).isoformat()

    for key, body, content_type in SAMPLE_FILES:
        pipeline.upload(key, body, content_type)
        print(f"✓ Uploaded: {key}")

    print("\nFile logs written by the Lambda:")
    for key, _, _ in SAMPLE_FILES:
        log = pipeline.wait_for_log(key, since)
        print(f"- {log['file_name']} | {log['file_size']} bytes | "
              f"{log['content_type']} | {log['upload_timestamp']}")


if __name__ == "__main__":
    main()
