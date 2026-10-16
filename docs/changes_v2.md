# Changes Made in poc-vet-agent-v2

## Overview
Created `poc-vet-agent-v2` alongside `poc-vet-agent` with the same file structure. Modified the HTTP server to handle **both GET and POST** requests on `/chat`.

## Files Modified

### 1. `bridge/http_server.py`
**Change**: Added `do_GET` method and refactored `_handle_chat` shared logic.

**Before (v1):**
- Only `do_POST` handled `/chat`
- Sending `GET http://localhost:5000/chat` returned `501 Unsupported method`

**After (v2):**
- Added `do_GET` method
- Extracted message parsing into `_handle_chat()`:
  - POST: reads from request body (JSON or raw)
  - GET: reads from query string (`?message=hello`)
- Both methods return same JSON response
- Updated `do_OPTIONS` to allow `GET, POST, OPTIONS`

**Example GET usage:**
```bash
curl "http://localhost:5000/chat?message=hello"
```

### 2. No other files changed
- `app/index.html`, `app/chat.css`, `app/chat.js` unchanged
- `config/vet_knowledge_base.json`, `config/agent_prompts.yaml` unchanged
- `data/vet_agent.db` unchanged (fresh copy from v1)
- `docs/` unchanged

## Server Status
- **Port 5000**: Old server (from `poc-vet-agent`) killed
- **New server**: Running from `/home/shiva/poc-vet-agent-v2/bridge/http_server.py`
- **Both GET and POST supported** on `http://localhost:5000/chat`

## How to Test
```bash
# GET (now working)
curl "http://localhost:5000/chat?message=hello"

# POST (still works)
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"hello"}'
```
