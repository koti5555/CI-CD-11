# Practical 11 — Observation and Evidence Record

| Test | Expected result | Verified result |
|---|---|---|
| Application startup | Model load INFO log | Verified in CI container log |
| GET /health | HTTP 200, request ID and duration | Passed in GitHub Actions |
| Valid POST /predict | HTTP 200 and prediction logs | PASS prediction test passed |
| Invalid POST /predict | HTTP 400 and validation WARNING | Passed; validation log detected |
| Unknown route | HTTP 404 and request log | Passed; 404 log detected |
| Request correlation | `X-Request-ID` response header | Verified by API test |
| Model training / quality gate | Training and accuracy >= 0.85 | Passed |
| Automated tests | ML and API tests | Passed |
| Docker build / run | Container starts and serves API | Passed |
| GHCR image publication | latest and SHA tag pushed | Passed in run 41324711127 |
| Render deployment | Existing service redeployed to new image | Pending manual Render dashboard action |
| Render runtime logs | Startup, success, validation and 404 events | Pending live service verification |

## Verified GHCR artifact

- Image: `ghcr.io/koti5555/student-result-prediction-ci-cd-11:latest`
- SHA image: `ghcr.io/koti5555/student-result-prediction-ci-cd-11:sha-4a7a8ce199c2faf7813b1c96e7b168216f134c36`
- Digest: `sha256:f687f3cae0574bc3454a437a0b0423071b7217bdcfdc12f5469c3dc561b9aeb8`
- Successful Actions run: https://github.com/koti5555/CI-CD-11/actions/runs/41324711127

## Compatibility note

The source Practical-9 API is Flask on port 5000, not FastAPI on port 8000. This continuation therefore returns HTTP 400 for invalid application payloads and does not provide Swagger `/docs` or FastAPI's automatic HTTP 422 response.

## Render verification procedure

After the image-backed Render service is manually redeployed to the image above, set `PORT=5000` and health check path `/health`. Send a valid POST to `/predict`, an invalid POST to `/predict`, and a request to a nonexistent route. Save the deployment ID, public endpoint, response codes, request IDs, and matching Render logs here. Never include secrets or student personal data.
