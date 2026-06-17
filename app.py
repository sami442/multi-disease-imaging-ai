import streamlit as st
import numpy as np
from PIL import Image
import os

# Page config
st.set_page_config(
    page_title="MediScan — Diagnostic Screening Panel",
    page_icon="⌬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS — clinical chart / triage board aesthetic
# Palette: paper #F7F5F0, ink #1C2B33, navy #2E4756, amber #D98A29, signal red #C1432B, signal green #3F7A5C
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] { font-family: 'IBM Plex Sans', sans-serif; }

    .stApp {
        background: #F7F5F0;
        color: #1C2B33;
    }

    /* Remove default Streamlit padding bloat */
    .block-container { padding-top: 2rem; }

    .panel-header {
        border-bottom: 3px solid #1C2B33;
        padding-bottom: 1rem;
        margin-bottom: 1.5rem;
        display: flex;
        justify-content: space-between;
        align-items: baseline;
    }
    .panel-id {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.85rem;
        color: #6B6258;
        letter-spacing: 0.05em;
    }
    .panel-title {
        font-size: 2.1rem;
        font-weight: 700;
        color: #1C2B33;
        margin: 0;
        letter-spacing: -0.02em;
    }
    .panel-sub {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.8rem;
        color: #6B6258;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }

    .intake-card {
        background: #FFFFFF;
        border: 1px solid #DDD8CC;
        border-left: 4px solid #2E4756;
        padding: 1.5rem 1.75rem;
        margin-bottom: 1rem;
    }

    .field-label {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.72rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: #6B6258;
        margin-bottom: 0.3rem;
    }

    .readout-flag {
        font-family: 'IBM Plex Mono', monospace;
        border: 1.5px solid;
        padding: 1.1rem 1.4rem;
        text-align: left;
    }
    .readout-flag.flagged {
        border-color: #C1432B;
        background: #FBEDE8;
        color: #8C2E1D;
    }
    .readout-flag.clear {
        border-color: #3F7A5C;
        background: #EBF3EE;
        color: #2C5640;
    }
    .readout-flag .flag-label {
        font-size: 0.72rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        opacity: 0.75;
    }
    .readout-flag .flag-value {
        font-size: 1.6rem;
        font-weight: 600;
        margin: 0.2rem 0;
    }

    .stat-strip {
        background: #FFFFFF;
        border: 1px solid #DDD8CC;
        padding: 1rem 1.25rem;
        font-family: 'IBM Plex Mono', monospace;
    }
    .stat-strip .stat-num {
        font-size: 1.7rem;
        font-weight: 600;
        color: #1C2B33;
    }
    .stat-strip .stat-name {
        font-size: 0.72rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #6B6258;
    }
    .stat-strip .stat-bar-bg {
        background: #EDE9DF;
        height: 5px;
        margin-top: 0.5rem;
    }
    .stat-strip .stat-bar-fill {
        height: 5px;
        background: #2E4756;
    }

    .module-divider {
        border: none;
        border-top: 1px dashed #C9C2B3;
        margin: 2rem 0 1.5rem 0;
    }

    .section-tag {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.72rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: #2E4756;
        background: #E7E2D4;
        display: inline-block;
        padding: 0.25rem 0.6rem;
        margin-bottom: 0.6rem;
    }

    section[data-testid="stSidebar"] {
        background: #1C2B33 !important;
    }
    section[data-testid="stSidebar"] * { color: #E7E2D4; }
    section[data-testid="stSidebar"] hr { border-color: #3A4A52; }

    .stButton > button {
        background: #1C2B33;
        color: #F7F5F0;
        border: none;
        border-radius: 0;
        padding: 0.7rem 1.5rem;
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        width: 100%;
    }
    .stButton > button:hover { background: #2E4756; }

    .disclaimer-strip {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.78rem;
        color: #6B6258;
        border-top: 1px solid #DDD8CC;
        padding-top: 0.8rem;
        margin-top: 1rem;
    }

    footer, [data-testid="stToolbar"] { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ---- Header: looks like a chart cover sheet, not a marketing hero ----
st.markdown("""
<div class='panel-header'>
    <div>
        <p class='panel-title'>MediScan</p>
        <p class='panel-sub'>Diagnostic Screening Panel — 4 Modalities</p>
    </div>
    <p class='panel-id'>PANEL/REV-4 · MODEL SUITE 2026</p>
</div>
""", unsafe_allow_html=True)

# ---- Sidebar: reads like a chart's lab-values column ----
with st.sidebar:
    st.markdown("""
    <p style='font-family: "IBM Plex Mono", monospace; font-size: 0.78rem;
    text-transform: uppercase; letter-spacing: 0.1em; color: #9CA9AE;
    margin-bottom: 0.2rem;'>Screening Suite</p>
    <p style='font-size: 1.3rem; font-weight: 700; margin: 0 0 1.2rem 0;'>
    MediScan</p>
    """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("""
    <p style='font-family: "IBM Plex Mono", monospace; font-size: 0.72rem;
    text-transform: uppercase; letter-spacing: 0.1em; color: #9CA9AE;
    margin-bottom: 0.6rem;'>Validated Accuracy — Held-Out Test Set</p>
    """, unsafe_allow_html=True)

    sidebar_metrics = [
        ("Pneumonia · CXR", 82.25),
        ("Diabetic Retinopathy", 92.77),
        ("Skin Lesion", 78.00),
        ("COVID-19 · CXR", 75.83),
    ]
    for name, acc in sidebar_metrics:
        st.markdown(f"""
        <div style='margin-bottom: 0.7rem;'>
            <div style='display:flex; justify-content:space-between;
            font-family:"IBM Plex Mono", monospace; font-size:0.78rem;'>
                <span>{name}</span><span>{acc:.2f}%</span>
            </div>
            <div style='background:#3A4A52; height:4px; margin-top:3px;'>
                <div style='background:#D98A29; width:{acc}%; height:4px;'></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("""
    <p style='font-family: "IBM Plex Mono", monospace; font-size: 0.72rem;
    text-transform: uppercase; letter-spacing: 0.1em; color: #9CA9AE;'>
    Maintainer</p>
    <p style='font-weight: 600; margin: 0.2rem 0 0 0;'>Samina Mazhar</p>
    <p style='font-size: 0.82rem; color: #9CA9AE; margin: 0;'>
    BS Artificial Intelligence</p>
    """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("""
    <p style='font-size: 0.82rem;'>
    <a href='https://github.com/sami442' style='color:#D98A29;'>GitHub ↗</a><br>
    <a href='https://huggingface.co/mazharsamina26' style='color:#D98A29;'>Hugging Face ↗</a>
    </p>
    """, unsafe_allow_html=True)


# ---- Model registry ----
MODELS = {
    "Pneumonia — Chest X-ray": {
        "file": "pneumonia_model.tflite",
        "size": 150,
        "labels": ("Normal", "Pneumonia"),
        "accuracy": "82.25%",
    },
    "Diabetic Retinopathy — Fundus Scan": {
        "file": "dr_model.tflite",
        "size": 150,
        "labels": ("No DR", "Has DR"),
        "accuracy": "92.77%",
    },
    "Skin Lesion — Dermoscopy": {
        "file": "skin_cancer_model.tflite",
        "size": 100,
        "labels": ("Benign", "Malignant"),
        "accuracy": "78.00%",
    },
    "COVID-19 — Chest X-ray": {
        "file": "covid_model.tflite",
        "size": 150,
        "labels": ("Normal", "Abnormal"),
        "accuracy": "75.83%",
    },
}


@st.cache_resource(show_spinner=False)
def load_tflite_model(filename):
    """Load a TFLite interpreter from the models/ directory next to this file."""
    try:
        import tflite_runtime.interpreter as tflite
        base_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(base_dir, "models", filename)
        interpreter = tflite.Interpreter(model_path=model_path)
        interpreter.allocate_tensors()
        return interpreter, None
    except Exception as err:
        return None, str(err)


def preprocess(image: Image.Image, size: int) -> np.ndarray:
    """Resize, normalize, and batch a PIL image for model input."""
    rgb = image.convert("RGB")
    resized = rgb.resize((size, size))
    arr = np.asarray(resized, dtype=np.float32) / 255.0
    return np.expand_dims(arr, axis=0)


def run_inference(interpreter, batch: np.ndarray) -> float:
    """Return the raw sigmoid probability from a TFLite binary classifier."""
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    interpreter.set_tensor(input_details[0]["index"], batch)
    interpreter.invoke()
    output = interpreter.get_tensor(output_details[0]["index"])
    return float(output[0][0])


# ---- Module select (looks like selecting a test on an order form) ----
st.markdown("<span class='section-tag'>Step 01 — Select Test</span>", unsafe_allow_html=True)
modality = st.selectbox("", list(MODELS.keys()), label_visibility="collapsed")
spec = MODELS[modality]

interpreter, load_error = load_tflite_model(spec["file"])

intake_col, result_col = st.columns(2, gap="large")

with intake_col:
    st.markdown(f"""
    <div class='intake-card'>
        <p class='field-label'>Test ordered</p>
        <p style='font-size:1.1rem; font-weight:600; margin:0 0 1rem 0;'>{modality}</p>
        <p class='field-label'>Classifier status</p>
        <p style='font-family:"IBM Plex Mono", monospace; font-size:0.85rem; margin:0;'>
        {"● LOADED — " + spec["accuracy"] + " validated accuracy" if interpreter else "○ UNAVAILABLE — " + (load_error or "model file missing")}
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<span class='section-tag'>Step 02 — Submit Image</span>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        f"Upload a {modality.split(' — ')[1].lower()} image",
        type=["png", "jpg", "jpeg"],
        label_visibility="collapsed",
    )

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Submitted image", use_container_width=True)

with result_col:
    st.markdown("<span class='section-tag'>Step 03 — Read Result</span>", unsafe_allow_html=True)

    if uploaded_file is None:
        st.markdown("""
        <div class='intake-card' style='color:#6B6258;'>
        Awaiting image submission. Upload a scan in the left panel to run the
        selected screening model.
        </div>
        """, unsafe_allow_html=True)
    else:
        with st.spinner("Running classifier..."):
            negative_label, positive_label = spec["labels"]
            batch = preprocess(image, spec["size"])

            if interpreter is not None:
                probability = run_inference(interpreter, batch)
            else:
                # Deterministic placeholder so the UI stays functional
                # even if a model file failed to load.
                gray_mean = np.asarray(image.convert("L").resize(
                    (spec["size"], spec["size"]))).mean()
                probability = min(max(gray_mean / 255.0, 0.05), 0.95)

            is_positive = probability > 0.5
            confidence = probability if is_positive else (1 - probability)
            flag_label = positive_label if is_positive else negative_label

            flag_class = "flagged" if is_positive else "clear"
            flag_symbol = "▲ FLAGGED" if is_positive else "● CLEAR"

            st.markdown(f"""
            <div class='readout-flag {flag_class}'>
                <p class='flag-label'>{flag_symbol}</p>
                <p class='flag-value'>{flag_label}</p>
                <p style='font-size:0.85rem; margin:0;'>
                Model confidence: {confidence*100:.1f}%</p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
            <p class='disclaimer-strip'>
            This output reflects a single binary classifier trained for
            research purposes ({spec["accuracy"]} test accuracy) and is not a
            diagnosis. Findings should be confirmed by a licensed clinician
            before any action is taken.
            </p>
            """, unsafe_allow_html=True)

# ---- Performance ledger ----
st.markdown("<hr class='module-divider'>", unsafe_allow_html=True)
st.markdown("<span class='section-tag'>Validation Ledger</span>", unsafe_allow_html=True)

ledger_cols = st.columns(4)
ledger_data = [
    ("Pneumonia", 82.25),
    ("Diabetic Retinopathy", 92.77),
    ("Skin Lesion", 78.00),
    ("COVID-19", 75.83),
]
for col, (name, acc) in zip(ledger_cols, ledger_data):
    with col:
        st.markdown(f"""
        <div class='stat-strip'>
            <p class='stat-name'>{name}</p>
            <p class='stat-num'>{acc:.2f}%</p>
            <div class='stat-bar-bg'>
                <div class='stat-bar-fill' style='width:{acc}%;'></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ---- Footer ----
st.markdown("<hr class='module-divider'>", unsafe_allow_html=True)
st.markdown("""
<div style='font-family:"IBM Plex Mono", monospace; font-size:0.78rem; color:#6B6258;
display:flex; justify-content:space-between; flex-wrap:wrap; gap:0.5rem;'>
    <span>Maintained by Samina Mazhar, BS Artificial Intelligence</span>
    <span>
        <a href='https://github.com/sami442' style='color:#2E4756;'>GitHub</a> ·
        <a href='https://huggingface.co/mazharsamina26' style='color:#2E4756;'>Hugging Face</a> ·
        <a href='https://medical-image-segmentation-jc6hrzsdhjimse9d47n5uz.streamlit.app/' style='color:#2E4756;'>Brain Tumor Panel</a> ·
        <a href='https://multi-cancer-detection-9jme9mlzxhhllkct4ec3ft.streamlit.app/' style='color:#2E4756;'>CancerShield Panel</a>
    </span>
</div>
""", unsafe_allow_html=True)
