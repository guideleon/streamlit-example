import altair as alt
import numpy as np
import pandas as pd
import streamlit as st
import run_model_py
"""
# Welcome to Streamlit!

Edit `/streamlit_app.py` to customize this app to your heart's desire :heart:.
If you have any questions, checkout our [documentation](https://docs.streamlit.io) and [community
forums](https://discuss.streamlit.io).

In the meantime, below is an example of what you can do with just a few lines of code:
"""


st.title("Aplicación de Streamlit")

# Ejecutar la función principal de run_model_py.py
data_usuario = run_model_py.capturar_entrada()
