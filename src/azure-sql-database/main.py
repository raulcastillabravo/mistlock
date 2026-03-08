import os
import io
import csv

from fastapi import FastAPI, Request
from dapr.clients import DaprClient

app = FastAPI()

# Input binding: /blob-input
@app.post("/blob-input")
async def process_blob(request: Request):
    """Triggered when a CSV is uploaded to Azurite."""
    # Read CSV data from request body
    content = (await request.body()).decode("utf-8")
    rows = csv.DictReader(io.StringIO(content))
    
    with DaprClient() as client:
        for row in rows:
            # Output binding: invoke sql-output to insert data
            sql_query = f"INSERT INTO users (name, email) VALUES ('{row['name']}', '{row['email']}')"
            client.invoke_binding(
                binding_name="sql-output",
                operation="exec",
                binding_metadata={"sql": sql_query},
                data=""
            )
    return {"status": "processed"}
