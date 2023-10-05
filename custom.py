import streamlit as st
import pandas as pd
import random, string


import streamlit as st
import pandas as pd
import random, string

# Generate DataFrame
num_rows = 100
SAID = [f"ID{str(i).zfill(4)}" for i in range(1, num_rows + 1)]
APP_Code = [''.join(random.choices(string.ascii_uppercase, k=3)) for _ in range(num_rows)]
Application_Name = [f"AppName{i}" for i in range(1, num_rows + 1)]
CWSS = [round(random.uniform(0, 10), 2) for _ in range(num_rows)]
Health_Score = [round(random.uniform(0, 100), 2) for _ in range(num_rows)]

data = pd.DataFrame({
    'SAID': SAID,
    'APP_Code': APP_Code,
    'Application_Name': Application_Name,
    'CWSS': CWSS,
    'Health_Score': Health_Score
})

score_to_filter = st.slider("Filter by Health Score", min_value=0.0, max_value=100.0, value=(0.0, 100.0))
filtered_data = data[(data['Health_Score'] >= score_to_filter[0]) & (data['Health_Score'] <= score_to_filter[1])]


table_header = """
    <table>
    <thead>
    <tr>
        <th style="background-color: green;">SAID</th>
        <th style='background-color: green;'>APP Code</th>
        <th style='background-color: green;'>CWSS</th>
        <th style='background-color: green;'>Application Name</th>
        <th style='background-color: red;'>Health Score</th>
    </tr>
    </thead>
    <tbody>
    
"""

tabledata = ""

for i in range(filtered_data.shape[0]):
    
    health_score = filtered_data.iloc[i, 4]
    
    
    if health_score <= 25:
        
        health_color = f'rgb(255, 0, 0)' # red
    
    elif health_score <= 50:
        health_color = f'rgb(255, 150, 0)' # orange
        
    elif health_score <= 75:
        health_color = f'rgb(255, 200, 0)' # yellow
        
    else:
        health_color = f'rgb(0, 200, 0)'
        

    tabledata += f"<tr><td>{filtered_data.iloc[i, 0]}</td><td>{filtered_data.iloc[i, 1]}</td><td>{filtered_data.iloc[i, 2]}</td><td>{filtered_data.iloc[i, 3]}</td><td style='background-color: {health_color};'>{health_score}</td></tr>"
    
table_foot = """
    </tbody>
    </table>
"""

finaltable = table_header + tabledata + table_foot

st.markdown(finaltable, unsafe_allow_html=True)
    