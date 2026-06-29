"""
04_streamlit/app.py
────────────────────
Full Streamlit dashboard that connects to the local FastAPI backend (api.py).

Features demonstrated:
  - st.cache_data(ttl=N)    — avoid hammering the API on every rerender
  - st.metric               — KPI tiles with delta
  - st.line_chart           — sparkline from metric history
  - st.dataframe            — sortable server table
  - st.form                 — register a new server without mid-typing reruns
  - st.session_state        — persist API key between reruns
  - st.empty + st.rerun     — live refresh loop with configurable interval

Run the API first:
    uvicorn api:app --reload --port 8004

Then:
    streamlit run app.py
"""

import time

import httpx
import pandas as pd
import streamlit as st

# ─── Config ───────────────────────────────────────────────────────────────────

API_BASE = "http://localhost:8004"
DEFAULT_KEY = "demo-key"

st.set_page_config(
    page_title="Server Dashboard",
    page_icon="🖥️",
    layout="wide",
)


# ─── Cached data fetchers ─────────────────────────────────────────────────────

@st.cache_data(ttl=2)
def fetch_metrics() -> dict:
    """
    Fetch live metrics from the API.
    Result is cached for 2 seconds — Streamlit can rerender many times
    per second; without this every render would call the API.
    """
    try:
        r = httpx.get(f"{API_BASE}/metrics", timeout=3.0)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        return {"error": str(e)}


@st.cache_data(ttl=5)
def fetch_metrics_history() -> list[dict]:
    """Fetch the rolling metrics history (cached 5s)."""
    try:
        r = httpx.get(f"{API_BASE}/metrics/history", timeout=3.0)
        r.raise_for_status()
        return r.json()
    except Exception:
        return []


@st.cache_data(ttl=5)
def fetch_servers(api_key: str) -> list[dict] | str:
    """Fetch the server list. Returns error string on failure."""
    try:
        r = httpx.get(
            f"{API_BASE}/servers",
            headers={"X-API-Key": api_key},
            timeout=3.0,
        )
        if r.status_code == 403:
            return "Invalid API key"
        r.raise_for_status()
        return r.json()
    except Exception as e:
        return str(e)


# ─── Sidebar ──────────────────────────────────────────────────────────────────

with st.sidebar:
    st.title("⚙️  Settings")

    if "api_key" not in st.session_state:
        st.session_state.api_key = DEFAULT_KEY

    st.session_state.api_key = st.text_input(
        "API Key", value=st.session_state.api_key, type="password"
    )

    refresh_interval = st.slider("Auto-refresh (s)", min_value=1, max_value=30, value=5)

    st.divider()

    # Register new server form
    st.subheader("➕  Register Server")
    with st.form("register_form", clear_on_submit=True):
        name = st.text_input("Name", placeholder="api-prod")
        host = st.text_input("Host", placeholder="10.0.0.1")
        port = st.number_input("Port", min_value=1, max_value=65535, value=8080)
        env  = st.selectbox("Environment", ["prod", "staging", "dev"])
        submitted = st.form_submit_button("Register")

    if submitted:
        if not name or not host:
            st.sidebar.error("Name and host are required.")
        else:
            try:
                r = httpx.post(
                    f"{API_BASE}/servers",
                    json={"name": name, "host": host, "port": port, "environment": env},
                    headers={"X-API-Key": st.session_state.api_key},
                    timeout=5.0,
                )
                if r.status_code == 201:
                    st.sidebar.success(f"Registered '{name}' (id={r.json()['id']})")
                    fetch_servers.clear()   # invalidate cache
                else:
                    st.sidebar.error(f"Error {r.status_code}: {r.text}")
            except Exception as e:
                st.sidebar.error(str(e))


# ─── Main content ─────────────────────────────────────────────────────────────

st.title("🖥️  Server Dashboard")

tab_metrics, tab_servers = st.tabs(["📊  System Metrics", "🗄️  Servers"])


# ── Metrics tab ───────────────────────────────────────────────────────────────
with tab_metrics:
    metrics = fetch_metrics()

    if "error" in metrics:
        st.error(f"Cannot reach API: {metrics['error']}")
        st.info("Make sure `uvicorn api:app --port 8004` is running.")
    else:
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("CPU",    f"{metrics['cpu_percent']:.1f}%")
        col2.metric("Memory", f"{metrics['memory_percent']:.1f}%",
                    f"{metrics['memory_used_gb']:.1f} / {metrics['memory_total_gb']:.1f} GB")
        col3.metric("Disk",   f"{metrics['disk_percent']:.1f}%")
        col4.metric("API",    "🟢 Online")

    # Sparkline from history
    history = fetch_metrics_history()
    if history:
        df = pd.DataFrame(history)
        df["time"] = pd.to_datetime(df["ts"], unit="s")
        df = df.set_index("time")[["cpu_percent", "memory_percent"]]
        st.line_chart(df, height=200)
        st.caption(f"Last {len(history)} seconds of CPU & memory")
    else:
        st.info("No history yet — metrics accumulate over time.")


# ── Servers tab ───────────────────────────────────────────────────────────────
with tab_servers:
    servers = fetch_servers(st.session_state.api_key)

    if isinstance(servers, str):
        st.error(f"Could not load servers: {servers}")
    elif not servers:
        st.info("No servers registered yet. Use the sidebar form to add one.")
    else:
        df = pd.DataFrame(servers)
        df["registered_at"] = pd.to_datetime(df["registered_at"], unit="s").dt.strftime("%Y-%m-%d %H:%M")
        st.dataframe(
            df[["id", "name", "host", "port", "environment", "registered_at"]],
            use_container_width=True,
            hide_index=True,
        )

        # Delete server
        with st.expander("🗑️  Delete a server"):
            ids = [s["id"] for s in servers]
            names = {s["id"]: f"[{s['id']}] {s['name']}" for s in servers}
            sel_id = st.selectbox("Select server", ids, format_func=lambda i: names[i])
            if st.button("Delete", type="primary"):
                try:
                    r = httpx.delete(
                        f"{API_BASE}/servers/{sel_id}",
                        headers={"X-API-Key": st.session_state.api_key},
                        timeout=5.0,
                    )
                    if r.status_code == 204:
                        st.success(f"Server {sel_id} deleted.")
                        fetch_servers.clear()
                        st.rerun()
                    else:
                        st.error(f"Error {r.status_code}: {r.text}")
                except Exception as e:
                    st.error(str(e))


# ─── Auto-refresh loop ────────────────────────────────────────────────────────

placeholder = st.empty()
with placeholder.container():
    st.caption(f"⏱ Auto-refreshing every {refresh_interval}s — last update: {time.strftime('%H:%M:%S')}")

time.sleep(refresh_interval)
st.rerun()
