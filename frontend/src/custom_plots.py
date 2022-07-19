import streamlit as st
import plotly.express as px


def plot_line(x, y):
    chart = px.line(x=x, y=y)
    st.plotly_chart(chart)
