from datetime import datetime, timezone

from src.file_pipeline import FilePipeline


def test_upload_is_logged_by_lambda():
    pipeline = FilePipeline()
    since = datetime.now(timezone.utc).isoformat()

    pipeline.upload("folder/my file.json", b'{"ok": true}', "application/json")
    log = pipeline.wait_for_log("folder/my file.json", since)

    assert log["file_name"] == "folder/my file.json"
    assert log["file_size"] == 12
    assert log["content_type"] == "application/json"
