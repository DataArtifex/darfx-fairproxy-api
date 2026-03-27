# Quickstart

## Overview

`fairproxy-api` exposes FAIR-oriented metadata and platform-native payloads
through a unified FastAPI interface.

Current Socrata support includes:

- Croissant metadata
- DCAT metadata
- DDI Codebook XML
- DDI-CDIF graphs
- Markdown summaries
- Postman collection generation
- Native dataset payloads through `/native`

## Run Locally

From the project directory:

```bash
uv sync
uv run uvicorn --app-dir src/dartfx fairproxy_api.main:app --host 0.0.0.0 --port 8000 --reload
```

From the monorepo root:

```bash
uv sync
uv run --package dartfx-fairproxy-api uvicorn --app-dir dartfx-fairproxy-api/src/dartfx fairproxy_api.main:app --host 0.0.0.0 --port 8000 --reload
```

Health check:

```bash
curl http://127.0.0.1:8000/status
```

## Endpoint Examples

### Current Top-Level Routes

- `/status` for health status
- `/servers` for configured data server discovery
- `/datasets/{uri}` for unified dataset metadata and native payloads
- `/socrata/{host}/{dataset_id}` for Socrata-specific dataset access

Generic routes like `/catalog`, `/resources`, and `/vocab` are intentionally not exposed in the current build.

### Socrata URI Format

The unified datasets endpoint expects Socrata URIs in this format:

`socrata:<server>:<dataset-id>`

Where:

- `socrata` is the platform identifier.
- `<server>` is the Socrata host (for example, `data.sfgov.org`).
- `<dataset-id>` is the Socrata dataset identifier (for example, `wg3w-h783`).

Example URI:

`socrata:data.sfgov.org:wg3w-h783`

### Unified dataset routes

```bash
curl "http://127.0.0.1:8000/datasets/socrata:data.sfgov.org:wg3w-h783/ddi/codebook"
curl "http://127.0.0.1:8000/datasets/socrata:data.sfgov.org:wg3w-h783/postman/collection"
curl "http://127.0.0.1:8000/datasets/socrata:data.sfgov.org:wg3w-h783/markdown"
curl "http://127.0.0.1:8000/datasets/socrata:data.sfgov.org:wg3w-h783/native"
```

### Socrata-specific routes

```bash
curl "http://127.0.0.1:8000/socrata/data.sfgov.org/wg3w-h783/ddi/codebook"
curl "http://127.0.0.1:8000/socrata/data.sfgov.org/wg3w-h783/native"
```

## Native Endpoint Convention

- `/datasets/{uri}/native` is the platform-agnostic native payload route.
- `/socrata/{host}/{dataset_id}/native` is the Socrata-specific native payload route.
- The previous `/socrata` native suffix is obsolete and has been replaced by `/native`.
