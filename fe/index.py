import time
import pandas as pd
import streamlit as st
from dotenv import load_dotenv

import os, sys

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(THIS_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from fe.api.prediction import build_base_url, healthcheck, get_pred


load_dotenv(dotenv_path=".dev.env")
st.set_page_config(page_title="Iris Prediction App", page_icon="🌸", layout="centered")

if "history" not in st.session_state:
    st.session_state.history = []

st.sidebar.header("Backend Settings")
host   = st.sidebar.text_input("Host", os.getenv("BE_APP_HOST", "127.0.0.1"))
port   = st.sidebar.text_input("Port", os.getenv("BE_APP_PORT", "8000"))
base_url = build_base_url(host, port)

col_hc1, col_hc2 = st.sidebar.columns([1, 1])
if col_hc1.button("Healthcheck"):
    ok, msg = healthcheck(base_url)
    if ok:
        st.sidebar.success(f"{msg} ✅")
    else:
        st.sidebar.error(msg)

st.sidebar.markdown("---")
st.sidebar.caption(f"Base URL: `{base_url}`")

st.title("Iris Prediction App")
st.write(
    "Masukkan fitur bunga Iris di bawah ini, lalu klik **Predict**. "
    "Aplikasi akan memanggil API FastAPI kamu dan menampilkan hasil prediksinya."
)
st.divider()

with st.expander("Preset Contoh (klik untuk autofill)"):
    c1, c2, c3 = st.columns(3)
    if c1.button("Setosa"):
        st.session_state["sl"] = 5.1; st.session_state["sw"] = 3.5
        st.session_state["pl"] = 1.4; st.session_state["pw"] = 0.2
    if c2.button("VersiColor"):
        st.session_state["sl"] = 5.9; st.session_state["sw"] = 3.0
        st.session_state["pl"] = 4.2; st.session_state["pw"] = 1.3
    if c3.button("Virginica"):
        st.session_state["sl"] = 6.7; st.session_state["sw"] = 3.1
        st.session_state["pl"] = 5.6; st.session_state["pw"] = 2.4

# default nilai
def _get_default(key, val): return st.session_state.get(key, val)

#form
with st.form("predict_form", clear_on_submit=False):
    st.subheader("Input Features")
    c1, c2 = st.columns(2)
    with c1:
        sepal_length = st.number_input("Sepal Length (cm)", min_value=0.0, max_value=10.0,
                                       value=float(_get_default("sl", 6.3)), step=0.1, format="%.1f")
        petal_length = st.number_input("Petal Length (cm)", min_value=0.0, max_value=10.0,
                                       value=float(_get_default("pl", 6.0)), step=0.1, format="%.1f")
    with c2:
        sepal_width  = st.number_input("Sepal Width (cm)",  min_value=0.0, max_value=10.0,
                                       value=float(_get_default("sw", 3.3)), step=0.1, format="%.1f")
        petal_width  = st.number_input("Petal Width (cm)",  min_value=0.0, max_value=10.0,
                                       value=float(_get_default("pw", 2.5)), step=0.1, format="%.1f")

    submitted = st.form_submit_button("Predict", use_container_width=True)

if submitted:
    # simpan ke session default agar preset mengisi ulang input
    st.session_state["sl"], st.session_state["sw"] = sepal_length, sepal_width
    st.session_state["pl"], st.session_state["pw"] = petal_length, petal_width

    # validasi ringan
    if any(v is None for v in [sepal_length, sepal_width, petal_length, petal_width]):
        st.error("Input tidak lengkap.")
    else:
        payload = {
            "sepal_length": float(sepal_length),
            "sepal_width":  float(sepal_width),
            "petal_length": float(petal_length),
            "petal_width":  float(petal_width),
        }
        with st.spinner("Mengirim permintaan ke API..."):
            try:
                msg, res = get_pred(payload, base_url=base_url)
                # Badge hasil
                label = (res or "").strip()
                if not label:
                    st.warning("API tidak mengembalikan label.")
                else:
                    # badge sederhana dengan warna per label
                    color = {"Setosa": "#16a34a", "VersiColor": "#eab308", "Virginica": "#2563eb"}.get(label, "#334155")
                    st.markdown(
                        f"""
                        <div style="display:flex;gap:.75rem;align-items:center;">
                          <span style="background:{color};color:white;padding:.4rem .6rem;border-radius:.5rem;">
                            {label}
                          </span>
                          <span style="opacity:.8">{msg or "Prediction ok"}</span>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    # tambah ke history
                    st.session_state.history.append({
                        "time": time.strftime("%Y-%m-%d %H:%M:%S"),
                        "sepal_length": sepal_length,
                        "sepal_width":  sepal_width,
                        "petal_length": petal_length,
                        "petal_width":  petal_width,
                        "result": label,
                    })
            except Exception as e:
                st.error(f"Gagal memproses prediksi: {e}")

if st.session_state.history:
    st.subheader("📝 Prediction History")
    hist_df = pd.DataFrame(st.session_state.history)
    st.dataframe(hist_df, use_container_width=True, hide_index=True)

st.markdown("---")
st.caption("Built with Streamlit · Connected to FastAPI · Iris demo")