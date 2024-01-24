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

st.title("Ingresar Datos para Predicción")

# Crear campos de entrada para los datos
Temperature = st.number_input("Temperatura", min_value=0.0)
Fuel_Price = st.number_input("Precio del Combustible", min_value=0.0)
CPI = st.number_input("CPI", min_value=0.0)
Unemployment = st.number_input("Tasa de Desempleo", min_value=0.0)
Size = st.number_input("Tamaño de la Tienda", min_value=0)
Store = st.number_input("Código de la Tienda (entre 1 y 45)", min_value=1, max_value=45)
Date = st.date_input("Fecha")
IsHoliday_True = st.checkbox("Es día festivo")

# Botón para realizar la predicción
if st.button("Realizar Predicción"):
    # Crear un DataFrame con los datos ingresados
    datos_entrada = pd.DataFrame([{
        'Temperature': Temperature,
        'Fuel_Price': Fuel_Price,
        'CPI': CPI,
        'Unemployment': Unemployment,
        'Size': Size,
        'Store': Store,
        'Date': Date,
        'IsHoliday_True': IsHoliday_True
    }])

    # Realizar la predicción aquí utilizando los datos ingresados en 'datos_entrada'
    # Puedes agregar el código de predicción en esta sección

    # Mostrar la predicción o resultado en Streamlit
    # Por ejemplo, puedes imprimir la predicción en la interfaz
    st.write("Resultado de la predicción:")
    st.write(datos_entrada)
