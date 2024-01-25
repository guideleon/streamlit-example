import altair as alt
import numpy as np
import pandas as pd
import streamlit as st
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

    # Crear columnas para one-hot encoding
    for i in range(1, 46):  # Para 45 tiendas
        datos_entrada[f'Store_{i}'] = 0  # Inicializar todas las columnas como 0

    # Establecer la columna correspondiente al valor de 'Store' como 1
    # Asegúrate de que 'Store' está en el DataFrame y contiene valores válidos
    if 'Store' in datos_entrada.columns:
        for index, row in datos_entrada.iterrows():
            if 1 <= row['Store'] <= 45:
                datos_entrada.at[index, f'Store_{row["Store"]}'] = 1

    # Extraer características de la fecha
    datos_entrada['Date'] = pd.to_datetime(datos_entrada['Date'])

    # Añadir columnas para cada mes
    for i in range(1, 13):  # Para todos los meses
        datos_entrada[f'Month_{i}'] = (datos_entrada['Date'].dt.month == i).astype(int)

    datos_entrada['Primera_quincena'] = (datos_entrada['Date'].dt.day <= 15).astype(int)

    # Eliminar columnas que ya no son necesarias
    datos_entrada.drop(['Store', 'Date'], axis=1, inplace=True)

    # Asegúrate de que el orden de las columnas sea el correcto
    columnas_modelo = [
        'IsHoliday_True',
        # Las columnas de las tiendas se añadirán aquí...
        'Month_1', 'Month_2', 'Month_3', 'Month_4', 'Month_5', 'Month_6', 'Month_7', 'Month_8',
        'Month_9', 'Month_10', 'Month_11', 'Month_12', 'Primera_quincena',
        'Temperature', 'Fuel_Price', 'CPI', 'Unemployment', 'Size'
    ]

    # Añadir columnas de tiendas
    columnas_tiendas = [f'Store_{i}' for i in range(1, 46)]  # Genera Store_1 hasta Store_45

    # Insertar las columnas de tiendas en la posición correcta
    posicion_insercion = 1  # Después de 'IsHoliday_True'
    for columna in columnas_tiendas:
        columnas_modelo.insert(posicion_insercion, columna)
        posicion_insercion += 1

    input = datos_entrada[columnas_modelo]
   
    # Cargar el modelo
    model = pickle.load(open('model.pkl', 'rb'))
    Prediccion = model.predict(input)
    Prediccion_str = str(Prediccion).strip('[]')

    Prediccion_str_con_separador = "{:,}".format(float(Prediccion_str))
    st.write("Resultado de la predicción:")
    st.write("Las ventas para las condiciones especificadas serán: ${} dólares".format(Prediccion_str_con_separador))
