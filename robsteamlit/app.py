import streamlit as st
import pandas as pd
import random, string
import numpy as np
from streamlit_option_menu import option_menu
import plotly.graph_objects as go
import plotly.express as px
import plotly.figure_factory as ff
from scipy import stats
from plotly.subplots import make_subplots
import plotly.subplots as sp


def summary(data, x):
    

    skew = data[x].skew()
    x_min, x_max = data[x].min(), data[x].max()
    Q1, Q2, Q3 = data[x].quantile(0.25), data[x].quantile(0.50), data[x].quantile(0.75)
    IQR = Q3 - Q1
    total_outlier_num = ((data[x] < (Q1 - 1.5 * IQR)) | (data[x] > (Q3 + 1.5 * IQR))).sum()

    st.text(
        f'7 Point Summary of {x.capitalize()} Attribute:\n'
        f'{x.capitalize()}(min) : {x_min}\n'
        f'Q1                    : {Q1}\n'
        f'Q2(Median)            : {Q2}\n'
        f'Q3                    : {Q3}\n'
        f'{x.capitalize()}(max) : {x_max}\n'
        f'Mean {x.capitalize()} = {data[x].mean()}\n'
        f'Median {x.capitalize()} = {data[x].median()}\n'
        f'Skewness of {x}: {skew}\n'
        # f'Total number of outliers in {x} distribution: {total_outlier_num}\n'
        )

    fig_density = px.histogram(data, x=x, marginal="rug", hover_data=data.columns)
    fig_density.add_vline(x=data[x].mean(), line_dash="dash", line_color="red", annotation_text="Mean")
    fig_density.add_vline(x=data[x].median(), line_dash="dash", line_color="green", annotation_text="Median")
    st.plotly_chart(fig_density)

    fig_violin = px.violin(data, y=x, box=True, points="all")
    fig_violin.add_trace(go.Scatter(y=data[x], mode='markers', name='Data Points'))
    st.plotly_chart(fig_violin)

    fig_box = go.Figure()
    fig_box.add_trace(go.Box(y=data[x], name=x))
    outliers = data[(data[x] < (Q1 - 1.5 * IQR)) | (data[x] > (Q3 + 1.5 * IQR))]
    for outlier in outliers[x]:
        fig_box.add_annotation(x=x, y=outlier, text="Outlier")
    st.plotly_chart(fig_box)

    percentiles = [50]
    fig_cdf = px.histogram(data, x=x, cumulative=True)
    for percentile in percentiles:
        value_at_percentile = data[x].quantile(percentile / 100)
        fig_cdf.add_hline(y=value_at_percentile, line_dash="dash", line_color="red", annotation_text=f"{percentile}%")
    st.plotly_chart(fig_cdf)


menu = ['Data filter','Labs','Visuals'] 

choice = option_menu(
    menu_title="Main Menu", options= menu,
    icons=['view-list', 'vinyl', 'patch-exclamation', 'fast-forward','save'],
    menu_icon = "chevron-double-left", default_index = 0, orientation = "vertical")


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

data

Visualsdata = data.select_dtypes(np.number)

if choice == 'Data filter':
    menu = list(Visualsdata.columns)
    
    filterchoice = st.selectbox("Data filter", menu)
    
# Filtering based on Health Score
    score_to_filter = st.slider("Filter by Health Score", min_value=0.0, max_value=100.0, value=(0.0, 100.0))
    filtered_data = data[(data[filterchoice] >= score_to_filter[0]) & (data[filterchoice] <= score_to_filter[1])]
    filtered_data

if choice == 'Labs':
    # HTML table
    table_header = """
        <table>
        <thead>
        <tr>
            <th style="color: green;">SAID</th>
            <th style="color: green;">APP Code</th>
            <th style="color: green;">Application Name</th>
            <th style="color: blue;">CWSS</th>
            <th style="color: red;">Health Score</th>
        </tr>
        </thead>
        <tbody>
    """

    table_data = ""
    for i in range(data.shape[0]):
        health_value = data.iloc[i, 4]
        # Color logic based on health_value
        if health_value <= 25:
            health_color = f'rgb(255, 0, 0)'  # Red

                    
        elif health_value <= 50:
            health_color = f'rgb(255, 165, 0)'  # Orange

            
        elif health_value <= 75:
            health_color = f'rgb(255, 255, 0)'  # Yellow

                    
        else:
            health_color = f'rgb(0, 255, 0)'  # Green


        table_data += f"<tr><td>{data.iloc[i, 0]}</td><td>{data.iloc[i, 1]}</td><td>{data.iloc[i, 2]}</td><td>{data.iloc[i, 3]}</td><td style='background-color: {health_color};'>{health_value}</td></tr>"

    table_footer = """
        </tbody>
        </table>
    """

    final_table = table_header + table_data + table_footer
    st.markdown(final_table, unsafe_allow_html=True)

if choice == 'Visuals':
    Visualsdata = data.select_dtypes(np.number)
    with st.expander('Feature Explorer'):
            variableToCheck = st.selectbox('Select Data Value', Visualsdata.columns.to_list())
            if variableToCheck:
                summary(Visualsdata.select_dtypes(np.number),variableToCheck)
