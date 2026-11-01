# Practical 11 — Observation and Evidence Record

| Test | Expected result | Evidence / observed result |
|---|---|---|
| Application startup | `event=model_loaded` | Pending workflow/runtime evidence |
| GET /health | HTTP 200, request ID, duration log | Pending |
| Valid POST /predict | HTTP 200, prediction request/success logs | Pending |
| Invalid POST /predict | HTTP 400 and `event=validation_error` warning | Pending |
| Unknown route | HTTP 404 warning | Pending |
| Request correlation | `X-Request-ID` response header | Pending |
| GitHub Actions | Tests, Docker build and publish succeed | Pending |
| GHCR | Updated latest and SHA-tagged image | Pending |
| Render | Redeployed service is live | Pending |
| Render runtime logs | Startup, success, validation and 404 events | Pending |

## Important compatibility note

The source Practical-9 API is Flask on port 5000, not FastAPI on port 8000. Consequently, this continuation uses HTTP 400 for invalid application payloads and does not provide Swagger `/docs` or FastAPI's automatic HTTP 422 response. Update this record only after each test is actually performed.
