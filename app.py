import logging
import os
import sys
import time
import uuid
from pathlib import Path

import joblib
import pandas as pd
from flask import Flask, g, jsonify, request

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
    force=True,
)
logger = logging.getLogger("student-result-api")

app = Flask(__name__)
MODEL_PATH = Path("student_result_model.pkl")
FEATURES = ["attendance", "internal_marks", "assignment_marks", "previous_score"]

try:
    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"{MODEL_PATH.name} was not found")
    model = joblib.load(MODEL_PATH)
    logger.info("event=model_loaded model_file=%s", MODEL_PATH.name)
except Exception:
    logger.exception("event=model_load_failed model_file=%s", MODEL_PATH.name)
    raise


@app.before_request
def start_request_logging():
    g.request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
    g.request_started = time.perf_counter()


@app.after_request
def finish_request_logging(response):
    request_id = getattr(g, "request_id", str(uuid.uuid4()))
    duration_ms = (time.perf_counter() - getattr(g, "request_started", time.perf_counter())) * 1000
    level = logging.WARNING if response.status_code >= 400 else logging.INFO
    logger.log(
        level,
        "event=http_request request_id=%s method=%s path=%s status=%s duration_ms=%.2f",
        request_id, request.method, request.path, response.status_code, duration_ms,
    )
    response.headers["X-Request-ID"] = request_id
    return response


@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    logger.exception("event=http_internal_error request_id=%s", getattr(g, "request_id", "unknown"))
    return jsonify({"error": "Internal server error"}), 500


@app.get("/")
@app.get("/health")
def health_check():
    return jsonify({"status": "ok", "service": "student-result-prediction"})


@app.post("/predict")
def predict():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        logger.warning("event=validation_error request_id=%s reason=invalid_json_or_missing_body",
                       getattr(g, "request_id", "unknown"))
        return jsonify({"error": "JSON request body is required"}), 400

    missing_fields = [feature for feature in FEATURES if feature not in data]
    if missing_fields:
        logger.warning(
            "event=validation_error request_id=%s field_locations=%s error_count=%s",
            getattr(g, "request_id", "unknown"), missing_fields, len(missing_fields),
        )
        return jsonify({"error": "Missing required fields", "missing_fields": missing_fields}), 400

    try:
        sample = pd.DataFrame([{feature: float(data[feature]) for feature in FEATURES}])
    except (TypeError, ValueError):
        logger.warning(
            "event=validation_error request_id=%s reason=non_numeric_feature",
            getattr(g, "request_id", "unknown"),
        )
        return jsonify({"error": "All feature values must be numeric"}), 400

    logger.info("event=prediction_request request_id=%s feature_names=%s",
                getattr(g, "request_id", "unknown"), sorted(FEATURES))
    try:
        prediction_code = int(model.predict(sample)[0])
        prediction = "PASS" if prediction_code == 1 else "FAIL"
        logger.info("event=prediction_success request_id=%s prediction=%s",
                    getattr(g, "request_id", "unknown"), prediction)
        return jsonify({"prediction": prediction, "prediction_code": prediction_code})
    except Exception:
        logger.exception("event=prediction_failed request_id=%s",
                         getattr(g, "request_id", "unknown"))
        return jsonify({"error": "Prediction failed"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "5000")))
