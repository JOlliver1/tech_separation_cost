import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
#import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Tech Separation Cost Dashboard",
                   page_icon=":bar_chart:",
                   layout="wide")


@st.cache
def get_data_from_excel():
    df = pd.read_excel('/Users/James/Desktop/TCS M&A/FinanceDashboard/fin_dashboard_xl.xls',
                            #engine='openpyxl',
                            sheet_name='Asset_Integration',
                            skiprows=8)
    return df


df = get_data_from_excel()
st.sidebar.header("Please Filter Here:")

project_name = st.sidebar.multiselect(
    "Select the Project Name:",
    options=df["ProjectName"].unique(),
    default=df["ProjectName"].unique()
)

application_name = st.sidebar.multiselect(
    "Select the Application / Task:",
    options=df["Application"].unique(),
    default=df["Application"].unique()
)

st.title("Tech Spearation Cost Dashboard")
st.markdown('---')

df_selection = df.query(
    "Application == @application_name & ProjectName == @project_name"
)

forecast_num1 = df["Forecasted costs by App"].sum()
forecast_num1 = forecast_num1*1.1
forecast_num = df_selection["Forecasted costs by App"].sum()
forecast_num = forecast_num*1.1

left_column, right_column = st.columns(2)
with left_column:
    st.metric('Forecast Total Spend', '£%.2f' % forecast_num1)
with right_column:
    st.metric('Forecast Total Spend of filtered apps', '£%.2f' % forecast_num)

st.markdown('---')
st.header('Overall Cost')

fig_product_sales = px.bar(
    df_selection,
    y="ProjectName",
    x='Cost',
    orientation="h",
    #title="<b>Overall Cost</b>",
    color_discrete_sequence=["#0083B8"] * len(df_selection),
    template="plotly_white",
    hover_name='Application'
)
fig_product_sales.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)


st.plotly_chart(fig_product_sales, use_container_width=True)

st.markdown('---')

nump_data = df.to_numpy()
cost = nump_data[:, 7]
name = nump_data[:, 4]

if st.checkbox('Show Apps with No Cost Data / Zero Cost'):
    for i in range(len(cost)):
        if cost[i] == 0:
            st.write(name[i])

