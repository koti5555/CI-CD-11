# MLOps Practical 11 — Application Logging and Error Tracking

## Continuity note

The actual Practical-9 source in `koti5555/CI-CD-9` is **Flask**, not FastAPI. It serves `/`, `/health`, and `/predict` on port **5000**. This repository preserves that API contract and adds logging without changing the model feature order or prediction pipeline.

The supplied FastAPI-only instructions (`/docs`, port 8000, and automatic HTTP 422 validation) do not match the existing deployed application. Invalid Flask payloads return HTTP 400; unknown routes return 404. Do not record Swagger/`/docs` or 422 as verified for this service.

## Logging added

- Model load success/failure at startup.
- Request ID from `X-Request-ID` or generated UUID.
- Method, path, status code, and response duration.
- Prediction request feature names and prediction result.
- Validation warnings without logging student identifiers or full payloads.
- Prediction exceptions with stack traces.
- Stdout logging for Docker and Render capture.

## API

- `GET /` and `GET /health`.
- `POST /predict` with numeric `attendance`, `internal_marks`, `assignment_marks`, and `previous_score`.
- Container port `5000`; Render variable `PORT=5000`.
- Every response includes `X-Request-ID`.

PASS:
```json
{"attendance":90,"internal_marks":85,"assignment_marks":88,"previous_score":80}
```

FAIL:
```json
{"attendance":55,"internal_marks":30,"assignment_marks":40,"previous_score":35}
```

## CI/CD

Push to `main` or manually run **Practical 11 - Logging, Test and Publish**. GitHub Actions trains the same deterministic classroom model, applies the 0.85 quality gate, runs ML/API tests, builds and tests the container, then publishes the tested image to GHCR.

Image reference retained from Practical 9:
`ghcr.io/koti5555/student-result-prediction-ci-cd-11:latest`

This repository publishes to its own GHCR package, `student-result-prediction-ci-cd-11`, to avoid needing write permission to the Practical-9 package. Never add a PAT or token to source files.

## Render redeployment

After a successful Actions run, manually deploy the latest image from the existing image-backed Render service. Keep the existing service, set `PORT=5000`, and use `/health` as the health check. Image-backed Render services may require Manual Deploy after the GHCR tag changes.

## Evidence

Record the successful Actions run, GHCR tag/digest, Render deployment ID, public health response, request IDs, and Render log evidence for successful requests, validation 400, and missing-route 404. Do not include student identifiers, tokens, or secrets.
