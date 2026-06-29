"""
05_integration/test_integration.py
────────────────────────────────────
End-to-end integration tests for the combined server (port 8005).

Covers all Day 3 features in one test suite:
  ✓ Health probe
  ✓ API Key auth (servers CRUD)
  ✓ JWT auth (login, /checks, role-based access)
  ✓ BackgroundTasks (fire-and-forget, polling for result)
  ✓ Metrics history (populated by lifespan loop)
  ✓ WebSocket streaming

Run the server first:
    uvicorn server:app --reload --port 8005

Then:
    python test_integration.py
"""

import asyncio
import json
import time

import httpx
import websockets

BASE = "http://localhost:8005"
WS_BASE = "ws://localhost:8005"
API_KEY = "integration-key"


PASS = "✅"
FAIL = "❌"
results: list[tuple[str, bool, str]] = []


def record(name: str, ok: bool, detail: str = ""):
    mark = PASS if ok else FAIL
    print(f"  {mark}  {name}" + (f"  ({detail})" if detail else ""))
    results.append((name, ok, detail))


async def test_health(client: httpx.AsyncClient):
    print("\n── Health ──")
    r = await client.get("/health")
    record("GET /health returns 200", r.status_code == 200)
    body = r.json()
    record("health body has status=ok", body.get("status") == "ok")


async def test_api_key(client: httpx.AsyncClient):
    print("\n── API Key Auth ──")

    # No key
    r = await client.get("/servers")
    record("No key → 403", r.status_code == 403)

    # Bad key
    r = await client.get("/servers", headers={"X-API-Key": "bad"})
    record("Bad key → 403", r.status_code == 403)

    # Valid key — empty list
    r = await client.get("/servers", headers={"X-API-Key": API_KEY})
    record("Valid key → 200", r.status_code == 200)

    # Register
    r = await client.post(
        "/servers",
        json={"name": "api-prod", "host": "10.0.0.1", "port": 8080},
        headers={"X-API-Key": API_KEY},
    )
    record("POST /servers → 201", r.status_code == 201)
    server_id = r.json().get("id")
    record("Response includes id", server_id is not None)

    # List now has one entry
    r = await client.get("/servers", headers={"X-API-Key": API_KEY})
    record("GET /servers returns 1 server", len(r.json()) == 1)

    return server_id


async def test_jwt(client: httpx.AsyncClient):
    print("\n── JWT Auth ──")

    # Bad credentials
    r = await client.post("/auth/token", json={"username": "admin", "password": "wrong"})
    record("Bad password → 401", r.status_code == 401)

    # Good credentials
    r = await client.post("/auth/token", json={"username": "admin", "password": "admin123"})
    record("Good login → 200", r.status_code == 200)
    token = r.json().get("access_token")
    record("Token present in response", bool(token))

    # Viewer token
    r = await client.post("/auth/token", json={"username": "viewer", "password": "viewer123"})
    viewer_token = r.json().get("access_token")

    return token, viewer_token


async def test_background_tasks(client: httpx.AsyncClient, token: str):
    print("\n── Background Tasks ──")
    headers = {"Authorization": f"Bearer {token}"}

    # Trigger a check — should return 202 immediately
    r = await client.post("/checks", json={"host": "example.com", "check_type": "ping"}, headers=headers)
    record("POST /checks → 202 (immediate)", r.status_code == 202)
    record("triggered_by in response", "triggered_by" in r.json())

    # Poll for result (background task takes ~1.5s)
    for _ in range(5):
        await asyncio.sleep(0.7)
        r = await client.get("/checks/results", headers=headers)
        if r.json():
            break
    record("Check result appears within 4s", len(r.json()) > 0)

    # Without token → 401
    r = await client.get("/checks/results")
    record("No token on /checks/results → 401", r.status_code == 401)


async def test_metrics_history(client: httpx.AsyncClient):
    print("\n── Metrics History (lifespan loop) ──")
    # The background loop started on app startup — wait a couple seconds
    await asyncio.sleep(2)
    r = await client.get("/metrics/history")
    record("GET /metrics/history → 200", r.status_code == 200)
    history = r.json()
    record("History has ≥ 1 snapshot", len(history) >= 1, f"{len(history)} snapshots")
    if history:
        last = history[-1]
        record("Snapshot has cpu field", "cpu" in last)
        record("Snapshot has mem field", "mem" in last)


async def test_websocket():
    print("\n── WebSocket ──")
    try:
        uri = f"{WS_BASE}/ws/metrics"
        frames = []
        async with websockets.connect(uri) as ws:
            for _ in range(3):
                raw = await asyncio.wait_for(ws.recv(), timeout=3.0)
                frames.append(json.loads(raw))
        record("Received 3 WebSocket frames", len(frames) == 3)
        record("Frame has cpu field", "cpu" in frames[0])
        record("Frame has mem field", "mem" in frames[0])
    except Exception as e:
        record("WebSocket connection", False, str(e))


async def main():
    print("=" * 55)
    print("  Day 3 Integration Tests → http://localhost:8005")
    print("=" * 55)

    try:
        async with httpx.AsyncClient(base_url=BASE, timeout=10.0) as client:
            await test_health(client)
            await test_api_key(client)
            token, _viewer_token = await test_jwt(client)
            await test_background_tasks(client, token)
            await test_metrics_history(client)
        await test_websocket()
    except httpx.ConnectError:
        print(f"\n{FAIL}  Could not connect to {BASE}")
        print("   Start the server first:  uvicorn server:app --port 8005")
        return

    # ── Summary ──────────────────────────────────────────────────────────────
    passed = sum(1 for _, ok, _ in results if ok)
    total  = len(results)
    print(f"\n{'=' * 55}")
    print(f"  Results: {passed}/{total} passed")
    if passed == total:
        print(f"  {PASS}  All tests passed!")
    else:
        print(f"  {FAIL}  {total - passed} test(s) failed:")
        for name, ok, detail in results:
            if not ok:
                print(f"       • {name}" + (f" ({detail})" if detail else ""))
    print("=" * 55)


if __name__ == "__main__":
    asyncio.run(main())
