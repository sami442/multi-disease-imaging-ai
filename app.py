import streamlit as st
import numpy as np
from PIL import Image
import requests
from io import BytesIO

# Page config
st.set_page_config(
    page_title="MediScan AI - Multi-Disease Detection",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Purple/Teal theme (different from other apps)
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        color: white;
    }
    .main-card {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(0,255,200,0.2);
        border-radius: 20px;
        padding: 2rem;
        backdrop-filter: blur(10px);
    }
    .disease-card {
        background: rgba(255,255,255,0.07);
        border: 1px solid rgba(0,255,200,0.15);
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.3s;
    }
    .disease-card:hover {
        border-color: rgba(0,255,200,0.5);
        transform: translateY(-3px);
    }
    .metric-box {
        background: rgba(0,255,200,0.08);
        border-radius: 12px;
        padding: 1.2rem;
        text-align: center;
        border-top: 3px solid #00ffc8;
    }
    .section-title {
        color: #00ffc8;
        font-size: 1.4rem;
        font-weight: 700;
        border-left: 4px solid #ff00aa;
        padding-left: 1rem;
        margin: 1.5rem 0 1rem 0;
    }
    .result-abnormal {
        background: linear-gradient(135deg, #ff416c, #ff4b2b);
        border-radius: 15px;
        padding: 1.5rem;
        color: white;
        text-align: center;
        font-weight: 700;
        box-shadow: 0 8px 20px rgba(255,65,108,0.3);
    }
    .result-normal {
        background: linear-gradient(135deg, #11998e, #38ef7d);
        border-radius: 15px;
        padding: 1.5rem;
        color: white;
        text-align: center;
        font-weight: 700;
        box-shadow: 0 8px 20px rgba(17,153,142,0.3);
    }
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f0c29, #302b63) !important;
    }
    .stButton > button {
        background: linear-gradient(135deg, #00ffc8, #00a8ff);
        color: #0f0c29;
        border: none;
        border-radius: 12px;
        padding: 0.8rem 2rem;
        font-weight: 700;
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class='main-card' style='text-align: center; margin-bottom: 2rem;'>
    <p style='font-size: 3rem; font-weight: 800;
    background: linear-gradient(90deg, #00ffc8, #ff00aa);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    margin: 0;'>🏥 MediScan AI</p>
    <p style='color: #b0b0d0; font-size: 1.1rem;'>
    Multi-Disease Detection from Medical Images using Deep Learning
    </p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("""
    <div style='text-align: center; padding: 1rem;'>
        <p style='font-size: 1.6rem;'>🏥</p>
        <p style='font-size: 1.3rem; font-weight: 700; color: #00ffc8;'>
        MediScan AI</p>
        <p style='color: #b0b0d0; font-size: 0.85rem;'>
        4 Diseases, 1 Dashboard</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <p style='color: #ff00aa; font-weight: 700; font-size: 0.9rem;'>
    📊 MODEL ACCURACY</p>
    """, unsafe_allow_html=True)

    accuracies = [
        ("🫁 Pneumonia", 82.25, "#00ffc8"),
        ("👁️ Diabetic Retinopathy", 92.77, "#00a8ff"),
        ("🔬 Skin Cancer", 78.00, "#ff00aa"),
        ("🦠 COVID-19", 75.83, "#ffaa00"),
    ]

    for name, acc, color in accuracies:
        st.markdown(f"""
        <div style='margin: 0.6rem 0;'>
            <p style='color: #e0e0f0; margin: 0; font-size: 0.85rem;'>{name}</p>
            <div style='background: rgba(255,255,255,0.1); border-radius: 10px; height: 8px;'>
                <div style='background: {color}; width: {acc}%; height: 8px; border-radius: 10px;'></div>
            </div>
            <p style='color: {color}; margin: 0; font-size: 0.8rem; text-align: right;'>{acc}%</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div style='background: rgba(255,255,255,0.07); border-radius: 12px; padding: 1rem;'>
        <p style='color: #00ffc8; font-weight: 700; margin: 0; font-size: 0.9rem;'>
        👩‍💻 DEVELOPER</p>
        <p style='color: white; font-weight: 700; margin: 0.3rem 0;'>Samina Mazhar</p>
        <p style='color: #b0b0d0; font-size: 0.8rem; margin: 0;'>BS Artificial Intelligence</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div style='text-align: center;'>
        <a href='https://github.com/sami442' style='color: #00ffc8;'>🐙 GitHub</a>
        &nbsp;|&nbsp;
        <a href='https://huggingface.co/mazharsamina26' style='color: #ff00aa;'>🤗 HuggingFace</a>
    </div>
    """, unsafe_allow_html=True)

# Load Models
@st.cache_resource
def load_tflite_model(model_name):
    try:
        import tflite_runtime.interpreter as tflite
        interpreter = tflite.Interpreter(model_path=f"models/{model_name}")
        interpreter.allocate_tensors()
        return interpreter
    except Exception as e:
        return None

models = {
    "🫁 Pneumonia (Chest X-ray)": {
        "file": "pneumonia_model.tflite",
        "size": 150,
        "labels": ["Normal", "Pneumonia"]
    },
    "👁️ Diabetic Retinopathy (Retina Scan)": {
        "file": "dr_model.tflite",
        "size": 150,
        "labels": ["No DR", "Has DR"]
    },
    "🔬 Skin Cancer (Dermoscopy)": {
        "file": "skin_cancer_model.tflite",
        "size": 100,
        "labels": ["Benign", "Malignant"]
    },
    "🦠 COVID-19 (Chest X-ray)": {
        "file": "covid_model.tflite",
        "size": 150,
        "labels": ["Normal", "Abnormal"]
    }
}

# Disease Selection
st.markdown("<p class='section-title'>🔬 Select Disease to Detect</p>", unsafe_allow_html=True)

disease_choice = st.selectbox("", list(models.keys()))

selected_model_info = models[disease_choice]
interpreter = load_tflite_model(selected_model_info["file"])

if interpreter:
    st.success(f"✅ {disease_choice} model loaded successfully!")
else:
    st.warning(f"⚠️ Model file not found - demo mode active")

st.markdown("<br>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("<p class='section-title'>📤 Upload Medical Image</p>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        f"Upload image for {disease_choice}",
        type=['png', 'jpg', 'jpeg']
    )

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_container_width=True)

with col2:
    st.markdown("<p class='section-title'>🎯 Analysis Result</p>", unsafe_allow_html=True)

    if uploaded_file is not None:
        with st.spinner("Analyzing image... ⏳"):
            IMG_SIZE = selected_model_info["size"]
            labels = selected_model_info["labels"]

            img_array = np.array(image.convert('RGB'))
            img_resized = np.array(
                Image.fromarray(img_array).resize((IMG_SIZE, IMG_SIZE))
            )
            img_normalized = (img_resized / 255.0).astype(np.float32)
            img_input = np.expand_dims(img_normalized, axis=0)

            if interpreter:
                input_details = interpreter.get_input_details()
                output_details = interpreter.get_output_details()
                interpreter.set_tensor(input_details[0]['index'], img_input)
                interpreter.invoke()
                prediction = interpreter.get_tensor(output_details[0]['index'])
                prob = float(prediction[0][0])
                pred_class = 1 if prob > 0.5 else 0
                confidence = prob if pred_class == 1 else (1 - prob)
            else:
                # Demo fallback
                gray = np.array(image.convert('L').resize((IMG_SIZE, IMG_SIZE)))
                pred_class = 1 if gray.mean() > 127 else 0
                confidence = 0.75

            result_label = labels[pred_class]

            if pred_class == 1:
                st.markdown(f"""
                <div class='result-abnormal'>
                ⚠️ {result_label.upper()}<br>
                <span style='font-size: 1.8rem;'>{confidence*100:.1f}%</span><br>
                confidence
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class='result-normal'>
                ✅ {result_label.upper()}<br>
                <span style='font-size: 1.8rem;'>{confidence*100:.1f}%</span><br>
                confidence
                </div>
                """, unsafe_allow_html=True)

            st.markdown("""
            <div style='background: rgba(255,255,255,0.05); border-radius: 10px;
            padding: 1rem; color: #b0b0d0; font-size: 0.85rem; margin-top: 1rem;'>
            ⚕️ <b>Disclaimer:</b> For research purposes only. 
            Always consult a medical professional for diagnosis.
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("👆 Upload an image to get started")

# Performance Overview
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<p class='section-title'>📊 All Models Performance</p>", unsafe_allow_html=True)

col3, col4, col5, col6 = st.columns(4)
metrics_data = [
    ("🫁 Pneumonia", "82.25%", col3),
    ("👁️ Diabetic Retinopathy", "92.77%", col4),
    ("🔬 Skin Cancer", "78.00%", col5),
    ("🦠 COVID-19", "75.83%", col6),
]

for name, acc, col in metrics_data:
    with col:
        st.markdown(f"""
        <div class='metric-box'>
            <p style='color: #b0b0d0; margin: 0; font-size: 0.85rem;'>{name}</p>
            <p style='color: #00ffc8; font-size: 1.8rem; font-weight: 800; margin: 0.3rem 0;'>{acc}</p>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div style='background: rgba(255,255,255,0.05); border-radius: 15px; 
padding: 2rem; text-align: center;'>
    <p style='color: white; font-size: 1.1rem; font-weight: 600; margin: 0;'>
    Developed with ❤️ by <span style='color: #00ffc8;'>Samina Mazhar</span></p>
    <p style='color: #b0b0d0; margin: 0.5rem 0;'>BS Artificial Intelligence</p>
    <p style='margin: 0;'>
    <a href='https://github.com/sami442' style='color: #00ffc8;'>🐙 GitHub</a> &nbsp;|&nbsp;
    <a href='https://huggingface.co/mazharsamina26' style='color: #ff00aa;'>🤗 HuggingFace</a> &nbsp;|&nbsp;
    <a href='https://medical-image-segmentation-jc6hrzsdhjimse9d47n5uz.streamlit.app/' style='color: #00a8ff;'>🧠 Brain Tumor App</a> &nbsp;|&nbsp;
    <a href='https://multi-cancer-detection-9jme9mlzxhhllkct4ec3ft.streamlit.app/' style='color: #ffaa00;'>🏥 CancerShield AI</a>
    </p>
</div>
""", unsafe_allow_html=True)
