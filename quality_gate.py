import json
import sys

with open("metrics.json", encoding="utf-8") as file:
    accuracy = json.load(file)["accuracy"]

print("Model accuracy:", round(accuracy, 4))
if accuracy < 0.85:
    print("QUALITY GATE FAILED")
    sys.exit(1)
print("QUALITY GATE PASSED")
