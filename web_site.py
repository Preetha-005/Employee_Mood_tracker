import streamlit as st
import pickle
import numpy as np
from PIL import Image
import base64

# Load the trained model
model_filename = "C:/Users/preet/OneDrive/Documents/intern/model.sav"
with open(model_filename, 'rb') as file:
    model = pickle.load(file)

# Streamlit UI
st.title('Employee Stress Prediction')
st.write('Enter employee details to predict stress levels')

# Input fields for features
employee_id = st.text_input('Employee ID')
date_time = st.number_input('Date', min_value=1, max_value=31, value=1)  # Restricting date input

# Inputs restricted to 1-10 (except caffeine intake, employee ID, physical activity)
workload_per_day = st.number_input('Workload Per Day (1-10)', min_value=1, max_value=10, value=1)
break_frequency = st.number_input('Break Frequency (1-10)', min_value=1, max_value=10, value=1)
sleep_hours = st.number_input('Sleep Hours (1-10)', min_value=1, max_value=10, value=1)
physical_activity = st.number_input('Physical Activity', value=0.0)  # No restriction
caffeine_intake = st.number_input('Caffeine Intake(mg)', value=0.0,max_value=400.0)  
stress_level = st.number_input('Mental Health (1-10)', min_value=1, max_value=10, value=1)

# Convert inputs into model-ready format
input_features = np.array([[employee_id, date_time, workload_per_day, break_frequency, sleep_hours, physical_activity, caffeine_intake, stress_level]])

# Image paths (ensure you have these images in the correct directory)
image_paths = {
    0: "C:/Users/preet/OneDrive/Documents/intern/Happy.jpg",  
    1: "C:/Users/preet/OneDrive/Documents/intern/Neutral.jpg",
    2: "C:/Users/preet/OneDrive/Documents/intern/Sad.jpg"     
}

# Function to encode image as base64
def get_base64_encoded_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Predict button
if st.button('Predict Stress Level'):
    try:
        prediction = model.predict(input_features)[0]
        stress_labels = {0: 'Happy', 1: 'Neutral', 2: 'Sad'}
        
        st.write(f'Predicted Stress Level: **{stress_labels[prediction]}**')

        # Display the corresponding image in the center
        if prediction in image_paths:
            image_base64 = get_base64_encoded_image(image_paths[prediction])
            st.markdown(
                f"""
                <div style="display: flex; justify-content: center;">
                    <img src="data:image/png;base64,{image_base64}" style="width: 250px; border-radius: 10px;">
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.write("No image available for this prediction.")

    except Exception as e:
        st.write(f"Error: {e}")
