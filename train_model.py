import json
import joblib
import numpy as np
import pandas as pd

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


def train_model():
    rng = np.random.default_rng(42)
    n = 300
    data = pd.DataFrame({
        "attendance": rng.integers(50, 101, n),
        "internal_marks": rng.integers(20, 101, n),
        "assignment_marks": rng.integers(30, 101, n),
        "previous_score": rng.integers(30, 101, n),
    })
    score = (
        0.25 * data["attendance"]
        + 0.35 * data["internal_marks"]
        + 0.20 * data["assignment_marks"]
        + 0.20 * data["previous_score"]
    )
    data["result"] = (score >= 60).astype(int)
    data.to_csv("student_results.csv", index=False)
    features = ["attendance", "internal_marks", "assignment_marks", "previous_score"]
    X_train, X_test, y_train, y_test = train_test_split(
        data[features], data["result"], test_size=0.20,
        random_state=42, stratify=data["result"]
    )
    model = Pipeline([
        ("scaler", StandardScaler()),
        ("classifier", LogisticRegression(max_iter=1000, random_state=42)),
    ])
    model.fit(X_train, y_train)
    accuracy = accuracy_score(y_test, model.predict(X_test))
    joblib.dump(model, "student_result_model.pkl")
    with open("metrics.json", "w", encoding="utf-8") as f:
        json.dump({"accuracy": float(accuracy)}, f, indent=4)
    print("Model accuracy:", round(accuracy, 4))


if __name__ == "__main__":
    train_model()
