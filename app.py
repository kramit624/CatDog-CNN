import streamlit as st
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
from PIL import Image
import pillow_avif  # Enables .avif support

# Load Model
model = load_model("cat_dog_classifier_vgg16_finetuned.h5")

# UI Title
st.title("🐶🐱 Cat vs Dog Classifier")
st.write("Upload an image and I will tell you whether it's a **Cat** or a **Dog**.")

# File Upload
uploaded_file = st.file_uploader(
    "Upload Image Here:",
    type=["jpg", "jpeg", "png", "webp", "avif"]
)

def predict(img):
    img = img.resize((150,150))
    x = image.img_to_array(img) / 255.0
    x = np.expand_dims(x, axis=0)
    pred = model.predict(x)[0][0]
    if pred >= 0.5:
        return "🐶 DOG", float(pred)
    else:
        return "🐱 CAT", float(1-pred)

if uploaded_file:
    # Show smaller image preview
    img = Image.open(uploaded_file)
    st.image(img, caption="Uploaded Image", width=300)

    # Predict button
    if st.button("Predict"):
        with st.spinner("Analyzing image... Please wait ⏳"):
            label, confidence = predict(img)

        st.success(f"Prediction: **{label}**")
        st.write(f"Confidence: **{confidence:.2f}**")
