import altair as alt
import numpy as np
import pandas as pd
import streamlit as st
import xgboost as xgb
import pickle

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

# Cargar el modelo
try:
    modelo_xgboost = xgb.Booster()
    modelo_xgboost.load_model('model.pkl')
except Exception as e:
    st.error(f"Error al cargar el modelo: {e}")
    model = None  # Asegura que el modelo es None si falla la carga

# Botón para realizar la predicción
if st.button("Realizar Predicción") and model is not None:
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

    # [El resto de tu código de preparación de datos va aquí...]

    # Realizar la predicción
    Prediccion = model.predict(input)
    Prediccion_str = str(Prediccion).strip('[]')
    Prediccion_str_con_separador = "{:,}".format(float(Prediccion_str))
    st.write("Resultado de la predicción:")
    st.write("Las ventas para las condiciones especificadas serán: ${} dólares".format(Prediccion_str_con_separador))
