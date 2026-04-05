import os
from flask import Flask, request, jsonify
from google.cloud import firestore
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

# In local dev, this connects automatically with FIRESTORE_EMULATOR_HOST
db = firestore.Client(project=os.getenv("GCP_PROJECT_ID", "demo-project"))

@app.route("/", methods=["POST"])
def admit_patient():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    data["admitted_at"] = firestore.SERVER_TIMESTAMP
    doc_ref = db.collection("patients").document(data["dni"])
    doc_ref.set(data)

    return jsonify({
        "status": "success",
        "message": f"Patient {data['name']} {data['surname']} admitted.",
        "patient_id": data["dni"]
    }), 201

if __name__ == "__main__":
    port = int(os.environ.get("SERVICE_PORT", 8080))
    app.run(host="0.0.0.0", port=port)
