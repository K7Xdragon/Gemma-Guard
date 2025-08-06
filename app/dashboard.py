import streamlit as st
from streamlit_autorefresh import st_autorefresh
import json
from datetime import datetime

from app.signal_engine import get_current_signal
from app.pattern_mapper import map_traits_to_behavioral_pattern
from app.matcher import match_signal_to_profile
from app.gemma_inference import run_inference
from app.insight_generator import generate_insight
from app.utils import load_json, append_json_line, ensure_dir

# --- Config
USER_PROFILE_PATH = "data/user_profile.json"
INFERENCE_LOG_PATH = "data/inference_log.json"
SIGNAL_LOG_PATH = "data/signal_log.json"

st.set_page_config(page_title="GemmaGuard Dashboard", layout="centered")

# --- Auto-refresh every 10 seconds
st_autorefresh(interval=10000, limit=100, key="signal_refresh")

# --- Header & Introduction
st.title("🧠 GemmaGuard")
st.caption("Burnout Signal Awareness & AI Insight System")

st.markdown("""
GemmaGuard was built to recognize burnout before it hits.  
By tracking simulated biometric signals and comparing them to personal behavioral traits,  
this app delivers insights that matter — even when you can't see them yet.
""")

# --- Load user profile and traits
user_profile = load_json(USER_PROFILE_PATH)
pattern_tags = map_traits_to_behavioral_pattern(user_profile.get("dob", "1990-01-01"))["pattern_tags"]

# --- Sidebar Panel
with st.sidebar:
    st.subheader("👤 Profile")
    st.write(f"Name: **{user_profile.get('name', 'User')}**")
    st.write("Traits:")
    st.json(user_profile.get("traits", {}), expanded=False)

    st.subheader("📎 Pattern Tags")
    st.write(pattern_tags)

# --- Signal Capture
st.session_state.latest_signal = get_current_signal()

# --- Display Signal
st.subheader("📡 Live Signal Snapshot")
st.json(st.session_state.latest_signal)

# --- Run Inference Button
if st.button("🧠 Run Inference"):
    ensure_dir("data")
    append_json_line(st.session_state.latest_signal, SIGNAL_LOG_PATH)

    with st.spinner("🧠 Gemma is analyzing the signal..."):
        progress_bar = st.progress(0)
        progress_bar.progress(10)

        match_result = match_signal_to_profile(st.session_state.latest_signal, pattern_tags)
        progress_bar.progress(40)

        inference = run_inference(pattern_tags, st.session_state.latest_signal)
        progress_bar.progress(70)

        insight = generate_insight(match_result, inference["inference"])
        progress_bar.progress(90)

        append_json_line({
            "timestamp": datetime.utcnow().isoformat(),
            "summary": insight["summary"],
            "recommendation": insight["recommendation"]
        }, INFERENCE_LOG_PATH)
        progress_bar.progress(100)

    st.success("✅ Inference Complete")
    st.markdown(f"**🧾 Summary:** {insight['summary']}")
    st.markdown(f"**🔮 Recommendation:** {insight['recommendation']}")

    with st.expander("🔧 Technical Details"):
        st.markdown(f"🔗 Signal ID: `{st.session_state.latest_signal.get('signal_id', 'N/A')}`")
        st.markdown(f"🧬 Model Reference: `{inference.get('llm_model', 'Unknown')}`")

# --- Inference Log History
st.divider()
st.subheader("📜 Inference History")

inference_log = load_json(INFERENCE_LOG_PATH, default=[])
if not inference_log:
    st.info("No previous inference yet.")
else:
    latest_logs = inference_log[-5:][::-1]
    for entry in latest_logs:
        with st.expander(f"🕒 {entry['timestamp']}"):
            st.write(f"**Summary:** {entry['summary']}")
            st.write(f"**Gemma Says:** {entry['recommendation']}")