# Day 3 — Streamlit


### 1. What is Streamlit?

Streamlit turns a plain Python script into an interactive web app. No HTML, CSS, or JavaScript required — you write Python and Streamlit renders the UI.

**How it works:**
- Every time the user interacts with a widget, the entire script reruns from top to bottom
- Streamlit tracks widget state and only re-renders what changed
- Results are displayed in the browser in real time

```bash
pip install streamlit
streamlit run dashboard.py
# → opens http://localhost:8501 in your browser
```

---

### 2. Page Setup & Layout

```python
import streamlit as st

# Must be the first Streamlit call in the script
st.set_page_config(
    page_title="DevOps Dashboard",
    page_icon="🖥️",
    layout="wide",          # use full browser width
    initial_sidebar_state="expanded",
)

st.title("🖥️ DevOps Monitoring Dashboard")
st.caption("Real-time metrics from the monitoring API")
```

#### Columns

```python
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("CPU", "45 %")

with col2:
    st.metric("Memory", "62 %")

with col3:
    st.metric("Disk", "38 %")
```

#### Sidebar

```python
with st.sidebar:
    st.header("Settings")
    api_url = st.text_input("API URL", value="http://localhost:8000")
    refresh_rate = st.slider("Refresh every (s)", min_value=1, max_value=30, value=5)
```

#### Tabs

```python
tab1, tab2 = st.tabs(["📊 Metrics", "🖥️ Servers"])

with tab1:
    st.write("Metrics content here")

with tab2:
    st.write("Servers content here")
```

---

### 3. Fetching Data from the FastAPI Backend

```python
import httpx

API_BASE = "http://localhost:8000"
API_KEY = "dev-secret-change-in-prod"
HEADERS = {"X-API-Key": API_KEY}


@st.cache_data(ttl=5)       # cache the result for 5 seconds
def fetch_metrics() -> dict:
    """Fetch current system metrics from the API."""
    try:
        resp = httpx.get(f"{API_BASE}/metrics", headers=HEADERS, timeout=5)
        resp.raise_for_status()
        return resp.json()
    except httpx.HTTPError as e:
        st.error(f"Failed to fetch metrics: {e}")
        return {}


@st.cache_data(ttl=5)
def fetch_servers() -> list[dict]:
    """Fetch the list of monitored servers."""
    try:
        resp = httpx.get(f"{API_BASE}/servers", headers=HEADERS, timeout=5)
        resp.raise_for_status()
        return resp.json()
    except httpx.HTTPError:
        return []
```

> `@st.cache_data(ttl=5)` caches the function result for 5 seconds. Without it, Streamlit would call the API on every rerender — potentially hundreds of times per minute.

---

### 4. Displaying Metrics

#### st.metric — Key Numbers

```python
metrics = fetch_metrics()

col1, col2, col3 = st.columns(3)

col1.metric(
    label="CPU Usage",
    value=f"{metrics.get('cpu_percent', 0):.1f} %",
    delta=f"{metrics.get('cpu_percent', 0) - 50:.1f} % vs baseline",
    delta_color="inverse",   # red when positive (high CPU is bad)
)
col2.metric("Memory", f"{metrics.get('memory_percent', 0):.1f} %")
col3.metric("Disk", f"{metrics.get('disk_percent', 0):.1f} %")
```

#### Progress Bars

```python
st.write("CPU")
st.progress(int(metrics.get("cpu_percent", 0)))

st.write("Memory")
st.progress(int(metrics.get("memory_percent", 0)))
```

---

### 5. Charts

#### Line Chart — Rolling Time Series

```python
import pandas as pd

# Build rolling history in session state
if "cpu_history" not in st.session_state:
    st.session_state.cpu_history = []

metrics = fetch_metrics()
st.session_state.cpu_history.append({
    "time": pd.Timestamp.now(),
    "cpu": metrics.get("cpu_percent", 0),
    "memory": metrics.get("memory_percent", 0),
})

# Keep last 60 samples
history = st.session_state.cpu_history[-60:]
df = pd.DataFrame(history).set_index("time")

st.subheader("CPU & Memory — Last 60 Samples")
st.line_chart(df)
```

#### Bar Chart

```python
servers = fetch_servers()
if servers:
    df = pd.DataFrame(servers)[["name", "response_time_ms"]].dropna()
    st.bar_chart(df.set_index("name"))
```

---

### 6. Tables

#### Static Table

```python
servers = fetch_servers()
if servers:
    df = pd.DataFrame(servers)
    st.dataframe(df, use_container_width=True)
```

#### Colour-Coded Status Table

```python
import pandas as pd

def colour_status(row):
    if row["status"] == "UP":
        return ["background-color: #d4edda"] * len(row)   # green
    elif row["status"] == "DEGRADED":
        return ["background-color: #fff3cd"] * len(row)   # yellow
    else:
        return ["background-color: #f8d7da"] * len(row)   # red

servers = fetch_servers()
if servers:
    df = pd.DataFrame(servers)
    st.dataframe(
        df.style.apply(colour_status, axis=1),
        use_container_width=True,
    )
```

---

### 7. Forms & User Input

Forms batch all inputs together and only trigger a rerun when the submit button is pressed — preventing partial updates on each keystroke.

```python
with st.form("register_server"):
    st.subheader("Register a Server")
    name = st.text_input("Name", placeholder="api-prod-1")
    host = st.text_input("Host", placeholder="10.0.0.1")
    port = st.number_input("Port", min_value=1, max_value=65535, value=8080)
    submitted = st.form_submit_button("Register")

if submitted:
    if not name or not host:
        st.error("Name and host are required.")
    else:
        try:
            resp = httpx.post(
                f"{API_BASE}/servers",
                json={"name": name, "host": host, "port": port},
                headers=HEADERS,
                timeout=5,
            )
            resp.raise_for_status()
            st.success(f"✅ Registered {name} ({host}:{port})")
            st.cache_data.clear()   # force servers list to refresh
        except httpx.HTTPError as e:
            st.error(f"Failed to register server: {e}")
```

#### Other Input Widgets

```python
# Buttons
if st.button("Refresh All"):
    st.cache_data.clear()
    st.rerun()

# Select box
selected_status = st.selectbox("Filter by status", ["All", "UP", "DEGRADED", "DOWN"])

# Checkbox
show_degraded = st.checkbox("Show degraded servers only", value=False)

# Text input with immediate effect
search = st.text_input("Search servers", placeholder="api...")
```

---

### 8. Session State

Streamlit reruns the script on every interaction. `st.session_state` persists values across reruns — like a per-user in-memory store.

```python
# Initialise once
if "servers" not in st.session_state:
    st.session_state.servers = []

if "selected_server_id" not in st.session_state:
    st.session_state.selected_server_id = None

# Update on interaction
if st.button("Select server 1"):
    st.session_state.selected_server_id = 1

# Read anywhere in the script
st.write(f"Selected: {st.session_state.selected_server_id}")
```

---

### 9. Auto-Refresh

Streamlit doesn't refresh automatically — you must trigger a rerun. The standard pattern is a `while True` loop with a placeholder:

```python
import time

placeholder = st.empty()   # reserve a spot in the layout

while True:
    with placeholder.container():
        metrics = fetch_metrics()
        col1, col2, col3 = st.columns(3)
        col1.metric("CPU", f"{metrics.get('cpu_percent', 0):.1f} %")
        col2.metric("Memory", f"{metrics.get('memory_percent', 0):.1f} %")
        col3.metric("Disk", f"{metrics.get('disk_percent', 0):.1f} %")

    time.sleep(2)
    st.rerun()
```

> `st.empty()` is key — without it each rerun appends new widgets below the old ones instead of replacing them.

---

### 10. Streamlit + WebSocket — Real-Time CPU Chart

For true WebSocket streaming (no polling), connect directly from Streamlit:

```python
import asyncio
import json
import websockets
import pandas as pd
import streamlit as st

async def stream_metrics(placeholder, n_frames: int = 60):
    history = []
    async with websockets.connect("ws://localhost:8000/ws/metrics") as ws:
        for _ in range(n_frames):
            data = json.loads(await ws.recv())
            history.append({"cpu": data["cpu_percent"], "memory": data["memory_percent"]})
            df = pd.DataFrame(history)
            with placeholder.container():
                st.line_chart(df)

chart_placeholder = st.empty()

if st.button("Start Live Stream"):
    asyncio.run(stream_metrics(chart_placeholder))
```
