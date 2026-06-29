"""
02_auth/client.py
──────────────────
Tests both API Key auth and JWT auth against the demo servers.

Usage:
    python client.py --mode apikey    # Test api_key_server.py (port 8001)
    python client.py --mode jwt       # Test jwt_server.py     (port 8002)
    python client.py --mode both      # Test both sequentially (default)
"""

import argparse
import asyncio

import httpx


# ─── API Key tests ────────────────────────────────────────────────────────────

async def test_api_key():
    base = "http://localhost:8001"
    print("\n" + "=" * 55)
    print("  API KEY AUTH  (server: api_key_server.py, port 8001)")
    print("=" * 55)

    async with httpx.AsyncClient(base_url=base, timeout=5.0) as client:

        # 1. No key → 403
        r = await client.get("/servers")
        print(f"\n[1] GET /servers  (no key)     → {r.status_code}  (expected 403)")
        assert r.status_code == 403, f"Expected 403, got {r.status_code}"

        # 2. Wrong key → 403
        r = await client.get("/servers", headers={"X-API-Key": "wrong-key"})
        print(f"[2] GET /servers  (bad key)    → {r.status_code}  (expected 403)")
        assert r.status_code == 403

        # 3. Valid key → 200 (empty list)
        key_a = "secret-key-123"
        r = await client.get("/servers", headers={"X-API-Key": key_a})
        print(f"[3] GET /servers  (valid key)  → {r.status_code}  {r.json()}")
        assert r.status_code == 200

        # 4. Register a server
        payload = {"name": "api-prod", "host": "10.0.0.1", "port": 8080}
        r = await client.post("/servers", json=payload, headers={"X-API-Key": key_a})
        print(f"[4] POST /servers              → {r.status_code}  {r.json()}")
        assert r.status_code == 201
        server_id = r.json()["id"]

        # 5. Team B cannot delete team A's server
        key_b = "another-key-456"
        r = await client.delete(f"/servers/{server_id}", headers={"X-API-Key": key_b})
        print(f"[5] DELETE /servers/{server_id} (team B) → {r.status_code}  (expected 403)")
        assert r.status_code == 403

        # 6. Team A can delete its own server
        r = await client.delete(f"/servers/{server_id}", headers={"X-API-Key": key_a})
        print(f"[6] DELETE /servers/{server_id} (team A) → {r.status_code}  (expected 204)")
        assert r.status_code == 204

    print("\n✅  All API key tests passed.")


# ─── JWT tests ────────────────────────────────────────────────────────────────

async def test_jwt():
    base = "http://localhost:8002"
    print("\n" + "=" * 55)
    print("  JWT AUTH  (server: jwt_server.py, port 8002)")
    print("=" * 55)

    async with httpx.AsyncClient(base_url=base, timeout=5.0) as client:

        # 1. No token → 401
        r = await client.get("/me")
        print(f"\n[1] GET /me  (no token)        → {r.status_code}  (expected 401)")
        assert r.status_code == 401

        # 2. Wrong password → 401
        r = await client.post("/auth/token", json={"username": "alice", "password": "wrong"})
        print(f"[2] POST /auth/token (bad pwd) → {r.status_code}  (expected 401)")
        assert r.status_code == 401

        # 3. Alice (admin) logs in
        r = await client.post("/auth/token", json={"username": "alice", "password": "password123"})
        print(f"[3] POST /auth/token (alice)   → {r.status_code}")
        assert r.status_code == 200
        alice_token = r.json()["access_token"]

        # 4. Alice can access /me
        r = await client.get("/me", headers={"Authorization": f"Bearer {alice_token}"})
        print(f"[4] GET /me (alice)            → {r.status_code}  {r.json()}")
        assert r.status_code == 200
        assert r.json()["role"] == "admin"

        # 5. Alice can access admin dashboard
        r = await client.get("/admin/dashboard", headers={"Authorization": f"Bearer {alice_token}"})
        print(f"[5] GET /admin/dashboard (alice) → {r.status_code}")
        assert r.status_code == 200

        # 6. Bob (viewer) logs in
        r = await client.post("/auth/token", json={"username": "bob", "password": "hunter2"})
        bob_token = r.json()["access_token"]

        # 7. Bob cannot access admin dashboard
        r = await client.get("/admin/dashboard", headers={"Authorization": f"Bearer {bob_token}"})
        print(f"[6] GET /admin/dashboard (bob) → {r.status_code}  (expected 403)")
        assert r.status_code == 403

        # 8. Invalid token → 401
        r = await client.get("/me", headers={"Authorization": "Bearer invalid.token.here"})
        print(f"[7] GET /me (garbage token)    → {r.status_code}  (expected 401)")
        assert r.status_code == 401

    print("\n✅  All JWT tests passed.")


# ─── Main ─────────────────────────────────────────────────────────────────────

async def main(mode: str):
    try:
        if mode in ("apikey", "both"):
            await test_api_key()
        if mode in ("jwt", "both"):
            await test_jwt()
    except httpx.ConnectError as e:
        print(f"\n❌  Connection failed: {e}")
        print("Make sure the relevant server is running first.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode", choices=["apikey", "jwt", "both"], default="both",
        help="Which auth server to test"
    )
    args = parser.parse_args()
    asyncio.run(main(args.mode))
