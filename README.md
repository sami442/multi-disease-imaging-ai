# 🏥 MediScan — Multi-Disease Screening Console

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.17-orange)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://multi-disease-imaging-ai.streamlit.app/)

## 🚀 Live Demo
👉 [**Try the App Here**](https://multi-disease-imaging-ai.streamlit.app/)

## 📌 Overview
MediScan is a multi-disease screening console built around four
independently trained CNN classifiers, each detecting a different
condition from medical imaging. Every model was trained on real,
published clinical datasets and converted to TensorFlow Lite for
lightweight deployment.

## 🎯 Supported Screening Tests
| Test | Modality | Dataset | Accuracy |
|------|----------|---------|----------|
| 🫁 Pneumonia | Chest X-ray | Kaggle Chest X-ray (Mooney) | 82.25% |
| 👁️ Diabetic Retinopathy | Fundus Scan | APTOS-2019 (Gaussian-filtered) | 92.77% |
| 🔬 Skin Lesion | Dermoscopy | HAM10000 | 78.00% |
| 🦠 COVID-19 | Chest X-ray | COVID-19 Radiography Database | 75.83% |

## 📊 Detailed Performance
| Test | Accuracy | Notes |
|------|----------|-------|
| Pneumonia | 82.25% | Binary: Normal vs Pneumonia |
| Diabetic Retinopathy | 92.77% | Binary: No DR vs Has DR (5-class APTOS simplified) |
| Skin Lesion | 78.00% | Binary: Benign vs Malignant (HAM10000 simplified), high recall on malignant class prioritized for screening safety |
| COVID-19 | 75.83% | Binary: Normal vs Abnormal (COVID + Lung Opacity + Viral Pneumonia combined) |

## ✨ App Features
- 🔬 Switch between 4 independent screening models from one console
- 📤 Upload your own medical image for any of the 4 modalities
- 🎯 Real-time TFLite inference with confidence score
- 📊 Validation ledger showing accuracy across all models
- ⚕️ Medical disclaimer on every result
- 🎨 Clinical-chart inspired interface

