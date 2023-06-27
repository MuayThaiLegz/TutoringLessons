import json
import os
import streamlit as st
import requests
from PIL import Image

# Set up the Streamlit app
st.title('Model prediction for Diabetes')
st.markdown('Please fill out this form')

# Get input data from Streamlit sidebar
age_mapping = {
    '25-29': 1,
    '30-34': 2,
    '35-39': 3,
    '40-44': 4,
    '45-49': 5,
    '50-54': 6,
    '55-59': 7,
    '60-64': 8,
    '65-69': 9,
    '70-74': 10,
    '75-79': 11,
    '80': 12
}
Age_input = st.sidebar.selectbox('Choose your age group', ['25-29', '30-34', '35-39', '40-44', '45-49', '50-54', '55-59', '60-64', '65-69', '70-74', '75-79', '80'])
age_numeric = age_mapping[Age_input]
Sex = st.sidebar.selectbox('Are you a male? 0=female, 1=male', [0, 1], 0)
HighChol = st.sidebar.selectbox('Have you had HighChol? 0=No, 1=High', [0, 1], 0)
CholCheck = st.sidebar.selectbox('Have you checked Chol in the past 5 years? 0=No, 1=Yes', [0, 1], 0)
Smoke = st.sidebar.selectbox('Have you smoked at least 100 cigarettes in your entire life? 0=No, 1=Yes', [0, 1], 0)
HeartDiseaseorAttack = st.sidebar.selectbox('Have you had a Heart Disease or Attack? 0=No, 1=Yes', [0, 1], 0)
PhysActivity = st.sidebar.selectbox('Have you had an illness or injury in the past 30 days? 0=No, 1=Yes', [0, 1], 0)
Fruits = st.sidebar.selectbox('Have you consumed fruit 1 or more times per day? 0=No, 1=Yes', [0, 1], 0)
Veggies = st.sidebar.selectbox('Have you eaten 1 or more veggies per day? 0=No, 1=Yes', [0, 1], 0)
HvyAlcoholConsump = st.sidebar.selectbox('Do you have heavy alcohol consumption? 0=No, 1=Yes', [0, 1], 0)
GenHlth = st.sidebar.selectbox('General health scale, 1=excellent, 2=very good, 3=good, 4=fair, 5=poor', [1,2,3,4,5], 0)
PhysHlth = st.sidebar.selectbox('Have you had physical health issues in the past 30 days (excluding job)? 0=No, 1=Yes', [0, 1], 0)
DiffWalk = st.sidebar.selectbox('Have you had difficulty walking or climbing stairs? 0=No, 1=Yes', [0, 1], 0)
Stroke = st.sidebar.selectbox('Have you had a stroke? 0=No, 1=Yes', [0, 1], 0)
HighBP = st.sidebar.selectbox('Have you had high blood pressure? 0=No, 1=Yes', [0, 1], 0)
BMI = st.sidebar.slider('What is your Body Mass Index?', 1, 100, 1)
MentHlth = st.sidebar.slider('Number of days of poor health in the past 30 days (scale 1-30)', 0, 30, 0)

# Create a dictionary from the input data
data = {
    'Age': age_numeric,
    'Sex': Sex,
    'HighChol': HighChol,
    'CholCheck': CholCheck,
    'BMI': BMI,
    'Smoke': Smoke,
    'HeartDiseaseorAttack': HeartDiseaseorAttack,
    'PhysActivity': PhysActivity,
    'Fruits': Fruits,
    'Veggies': Veggies,
    'HvyAlcoholConsump': HvyAlcoholConsump,
    'GenHlth': GenHlth,
    'MentHlth': MentHlth,
    'PhysHlth': PhysHlth,
    'DiffWalk': DiffWalk,
    'Stroke': Stroke,
    'HighBP': HighBP,
}

# Convert the dictionary to JSON data
data_json = json.dumps(data)

# Make a prediction by sending a request to the API
api_url = os.environ.get("API_URL", "http://api:8000")
pred = requests.post(url=f"{api_url}/prediction", json=data)

if st.button('Predict'):
    
    st.write(pred.text)
    st.subheader("Based on the provided data, the prediction is:")
    result = " "
    if pred.text == 'healthy':
        result = 'healthy'
    else:
        result = 'not healthy'
    
if st.checkbox("Show details"):
    st.write("The data retrieved from the Streamlit frontend: the user input is converted into a JSON object and sent to the API's endpoint.")
    st.table(data)
