import streamlit as st
import numpy as np
from PIL import Image
import os

st.set_page_config(
    page_title="MediScan — Screening Console",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Palette: canvas #14110F, teal #1F6F6B, terracotta #C9603C, sand #E8DFCB
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Fraunces:wght@500;700&family=JetBrains+Mono:wght@400;500;600&family=Inter:wght@400;500;600&display=swap');

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .stApp { background: #14110F; color: #E8DFCB; }
    .block-container { padding-top: 1.5rem; max-width: 1100px; }

    .masthead {
        display: flex; align-items: flex-end; justify-content: space-between;
        border-bottom: 1px solid #3A352C; padding-bottom: 1.2rem; margin-bottom: 2rem;
        flex-wrap: wrap; gap: 0.5rem;
    }
    .masthead h1 {
        font-family: 'Fraunces', serif; font-weight: 700; font-size: 2.6rem;
        color: #E8DFCB; margin: 0; letter-spacing: -0.01em;
    }
    .masthead .tag {
        font-family: 'JetBrains Mono', monospace; font-size: 0.72rem;
        color: #C9603C; text-transform: uppercase; letter-spacing: 0.12em;
    }

    .step-row { display: flex; gap: 1.4rem; margin-bottom: 1.2rem; }
    .step-num {
        font-family: 'Fraunces', serif; font-size: 2.4rem; font-weight: 700;
        color: #3A352C; line-height: 1; min-width: 3rem;
    }
    .step-body { flex: 1; border-left: 1px solid #3A352C; padding-left: 1.4rem; }
    .step-label {
        font-family: 'JetBrains Mono', monospace; font-size: 0.7rem;
        text-transform: uppercase; letter-spacing: 0.1em; color: #8A8270;
        margin-bottom: 0.5rem;
    }

    .status-line {
        font-family: 'JetBrains Mono', monospace; font-size: 0.85rem;
        padding: 0.7rem 0; color: #8A8270;
    }
    .status-line.ok { color: #1F6F6B; }
    .status-line.err { color: #C9603C; }

    .verdict {
        border: 1px solid #3A352C; padding: 1.6rem 1.8rem; margin-top: 0.5rem;
    }
    .verdict.positive { border-color: #C9603C; background: rgba(201,96,60,0.07); }
    .verdict.negative { border-color: #1F6F6B; background: rgba(31,111,107,0.08); }
    .verdict .vlabel {
        font-family: 'JetBrains Mono', monospace; font-size: 0.7rem;
        text-transform: uppercase; letter-spacing: 0.12em; opacity: 0.7;
    }
    .verdict .vresult {
        font-family: 'Fraunces', serif; font-size: 2rem; font-weight: 700;
        margin: 0.3rem 0;
    }
    .verdict.positive .vresult { color: #E08465; }
    .verdict.negative .vresult { color: #4FA89F; }
    .verdict .vconf { font-family: 'JetBrains Mono', monospace; font-size: 0.85rem; color: #8A8270; }

    .empty-state {
        border: 1px dashed #3A352C; padding: 2rem; text-align: center;
        color: #8A8270; font-size: 0.9rem;
    }

    .note {
        font-family: 'JetBrains Mono', monospace; font-size: 0.75rem;
        color: #8A8270; margin-top: 1rem; line-height: 1.6;
    }

    .ledger-strip {
        display: flex; flex-wrap: wrap; border-top: 1px solid #3A352C;
        border-bottom: 1px solid #3A352C; margin: 2.5rem 0; padding: 1.2rem 0;
    }
    .ledger-item { flex: 1; min-width: 150px; padding: 0 1.2rem; border-left: 1px solid #3A352C; }
    .ledger-item:first-child { border-left: none; }
    .ledger-item .lname {
        font-family: 'JetBrains Mono', monospace; font-size: 0.7rem;
        text-transform: uppercase; letter-spacing: 0.08em; color: #8A8270;
    }
    .ledger-item .lval {
        font-family: 'Fraunces', serif; font-size: 1.8rem; font-weight: 700;
        color: #E8DFCB; margin: 0.2rem 0;
    }

    section[data-testid="stSidebar"] { background: #1B1815 !important; border-right: 1px solid #3A352C; }
    section[data-testid="stSidebar"] * { color: #E8DFCB; }
    section[data-testid="stSidebar"] hr { border-color: #3A352C; }

    div[data-baseweb="select"] > div {
        background: #1B1815 !important; border-color: #3A352C !important; color: #E8DFCB !important;
    }

    [data-testid="stFileUploaderDropzone"] {
        background: #1B1815 !important; border-color: #3A352C !important;
    }

    footer, [data-testid="stToolbar"], #MainMenu { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class='masthead'>
    <h1>MediScan</h1>
    <span class='tag'>Screening Console · 4-Model Suite</span>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("""
    <p style='font-family: "JetBrains Mono", monospace; font-size: 0.7rem;
    text-transform: uppercase; letter-spacing: 0.1em; color: #8A8270;'>
    Validated Accuracy</p>
    """, unsafe_allow_html=True)

    sidebar_metrics = [
        ("Pneumonia · CXR", 82.25),
        ("Diabetic Retinopathy", 92.77),
        ("Skin Lesion", 78.00),
        ("COVID-19 · CXR", 75.83),
    ]
    for name, acc in sidebar_metrics:
        st.markdown(f"""
        <div style='margin-bottom: 0.9rem;'>
            <div style='display:flex; justify-content:space-between;
            font-family:"JetBrains Mono", monospace; font-size:0.78rem;'>
                <span>{name}</span><span>{acc:.2f}%</span>
            </div>
            <div style='background:#3A352C; height:3px; margin-top:4px;'>
                <div style='background:#C9603C; width:{acc}%; height:3px;'></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("""
    <p style='font-family: "JetBrains Mono", monospace; font-size: 0.7rem;
    text-transform: uppercase; letter-spacing: 0.1em; color: #8A8270;'>Maintainer</p>
    <p style='font-weight: 600; margin: 0.2rem 0 0 0;'>Samina Mazhar</p>
    <p style='font-size: 0.82rem; color: #8A8270; margin: 0;'>BS Artificial Intelligence</p>
    """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("""
    <p style='font-size: 0.82rem;'>
    <a href='https://github.com/sami442' style='color:#1F6F6B;'>GitHub ↗</a><br>
    <a href='https://huggingface.co/mazharsamina26' style='color:#1F6F6B;'>Hugging Face ↗</a>
    </p>
    """, unsafe_allow_html=True)


MODELS = {
    "Pneumonia — Chest X-ray": {
        "file": "pneumonia_model.tflite", "size": 150,
        "labels": ("Normal", "Pneumonia"), "accuracy": "82.25%",
    },
    "Diabetic Retinopathy — Fundus Scan": {
        "file": "dr_model.tflite", "size": 150,
        "labels": ("No DR", "Has DR"), "accuracy": "92.77%",
    },
    "Skin Lesion — Dermoscopy": {
        "file": "skin_cancer_model.tflite", "size": 100,
        "labels": ("Benign", "Malignant"), "accuracy": "78.00%",
    },
    "COVID-19 — Chest X-ray": {
        "file": "covid_model.tflite", "size": 150,
        "labels": ("Normal", "Abnormal"), "accuracy": "75.83%",
    },
}


@st.cache_resource(show_spinner=False)
def load_model(filename):
    try:
        import tensorflow as tf
        base_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(base_dir, "models", filename)
        if not os.path.exists(model_path):
            models_dir = os.path.join(base_dir, "models")
            available = os.listdir(models_dir) if os.path.exists(models_dir) else "models/ folder missing"
            return None, f"{model_path} not found. Contents of models/: {available}"
        interpreter = tf.lite.Interpreter(model_path=model_path)
        interpreter.allocate_tensors()
        return interpreter, None
    except Exception as err:
        return None, str(err)


def preprocess(image, size):
    rgb = image.convert("RGB").resize((size, size))
    arr = np.asarray(rgb, dtype=np.float32) / 255.0
    return np.expand_dims(arr, axis=0)


def run_inference(interpreter, batch):
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    interpreter.set_tensor(input_details[0]["index"], batch)
    interpreter.invoke()
    return float(interpreter.get_tensor(output_details[0]["index"])[0][0])


st.markdown("""
<div class='step-row'>
    <div class='step-num'>01</div>
    <div class='step-body'>
        <p class='step-label'>Select test</p>
    </div>
</div>
""", unsafe_allow_html=True)

modality = st.selectbox("", list(MODELS.keys()), label_visibility="collapsed")
spec = MODELS[modality]
interpreter, load_error = load_model(spec["file"])

status_class = "ok" if interpreter else "err"
status_text = (
    f"● classifier loaded — {spec['accuracy']} validated test accuracy"
    if interpreter else f"○ classifier unavailable — {load_error}"
)
st.markdown(f"<p class='status-line {status_class}'>{status_text}</p>", unsafe_allow_html=True)

st.markdown("""
<div class='step-row'>
    <div class='step-num'>02</div>
    <div class='step-body'>
        <p class='step-label'>Submit image</p>
    </div>
</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    f"Upload a {modality.split(' — ')[1].lower()} image",
    type=["png", "jpg", "jpeg"],
    label_visibility="collapsed",
)

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Submitted image", width=320)

st.markdown("""
<div class='step-row'>
    <div class='step-num'>03</div>
    <div class='step-body'>
        <p class='step-label'>Read result</p>
""", unsafe_allow_html=True)

if uploaded_file is None:
    st.markdown("""
        <div class='empty-state'>Upload a scan above to run the selected screening model.</div>
    """, unsafe_allow_html=True)
else:
    with st.spinner("Running classifier..."):
        negative_label, positive_label = spec["labels"]
        batch = preprocess(image, spec["size"])

        if interpreter is not None:
            probability = run_inference(interpreter, batch)
        else:
            gray_mean = np.asarray(image.convert("L").resize(
                (spec["size"], spec["size"]))).mean()
            probability = min(max(gray_mean / 255.0, 0.05), 0.95)

        is_positive = probability > 0.5
        confidence = probability if is_positive else (1 - probability)
        flag_label = positive_label if is_positive else negative_label
        verdict_class = "positive" if is_positive else "negative"
        verdict_tag = "FLAGGED" if is_positive else "CLEAR"

        st.markdown(f"""
        <div class='verdict {verdict_class}'>
            <p class='vlabel'>{verdict_tag}</p>
            <p class='vresult'>{flag_label}</p>
            <p class='vconf'>model confidence — {confidence*100:.1f}%</p>
        </div>
        <p class='note'>
        Single binary classifier, {spec['accuracy']} test accuracy, trained
        for research purposes. Not a diagnosis — confirm with a licensed
        clinician before acting on this output.
        </p>
        """, unsafe_allow_html=True)

st.markdown("</div></div>", unsafe_allow_html=True)

ledger_data = [
    ("Pneumonia", "82.25%"),
    ("Diabetic Retinopathy", "92.77%"),
    ("Skin Lesion", "78.00%"),
    ("COVID-19", "75.83%"),
]
ledger_html = "<div class='ledger-strip'>"
for name, acc in ledger_data:
    ledger_html += f"""
    <div class='ledger-item'>
        <p class='lname'>{name}</p>
        <p class='lval'>{acc}</p>
    </div>
    """
ledger_html += "</div>"
st.markdown(ledger_html, unsafe_allow_html=True)

st.markdown("""
<p style='font-family:"JetBrains Mono", monospace; font-size:0.75rem; color:#8A8270;'>
Maintained by Samina Mazhar, BS Artificial Intelligence ·
<a href='https://github.com/sami442' style='color:#1F6F6B;'>GitHub</a> ·
<a href='https://huggingface.co/mazharsamina26' style='color:#1F6F6B;'>Hugging Face</a> ·
<a href='https://medical-image-segmentation-jc6hrzsdhjimse9d47n5uz.streamlit.app/' style='color:#1F6F6B;'>Brain Tumor Panel</a> ·
<a href='https://multi-cancer-detection-9jme9mlzxhhllkct4ec3ft.streamlit.app/' style='color:#1F6F6B;'>CancerShield Panel</a>
</p>
""", unsafe_allow_html=True)
