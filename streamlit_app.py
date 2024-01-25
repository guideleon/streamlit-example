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

@@ -41,58 +31,51 @@
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
    for i in range(1, 46):  # Para 45 tiendas
        datos_entrada[f'Store_{i}'] = 0  # Inicializar todas las columnas como 0

# Añadir columnas para cada mes
for i in range(1, 13):  # Para todos los meses
    datos_entrada[f'Month_{i}'] = (datos_entrada['Date'].dt.month == i).astype(int)
    # Establecer la columna correspondiente al valor de 'Store' como 1
    # Asegúrate de que 'Store' está en el DataFrame y contiene valores válidos
    if 'Store' in datos_entrada.columns:
        for index, row in datos_entrada.iterrows():
            if 1 <= row['Store'] <= 45:
                datos_entrada.at[index, f'Store_{row["Store"]}'] = 1

datos_entrada['Primera_quincena'] = (datos_entrada['Date'].dt.day <= 15).astype(int)
    # Extraer características de la fecha
    datos_entrada['Date'] = pd.to_datetime(datos_entrada['Date'])

# Eliminar columnas que ya no son necesarias
datos_entrada.drop(['Store', 'Date'], axis=1, inplace=True)
    # Añadir columnas para cada mes
    for i in range(1, 13):  # Para todos los meses
        datos_entrada[f'Month_{i}'] = (datos_entrada['Date'].dt.month == i).astype(int)

# Asegúrate de que el orden de las columnas sea el correcto
columnas_modelo = [
    'IsHoliday_True',
    # Las columnas de las tiendas se añadirán aquí...
    'Month_1', 'Month_2', 'Month_3', 'Month_4', 'Month_5', 'Month_6', 'Month_7', 'Month_8',
    'Month_9', 'Month_10', 'Month_11', 'Month_12', 'Primera_quincena',
    'Temperature', 'Fuel_Price', 'CPI', 'Unemployment', 'Size'
]
    datos_entrada['Primera_quincena'] = (datos_entrada['Date'].dt.day <= 15).astype(int)

# Añadir columnas de tiendas
columnas_tiendas = [f'Store_{i}' for i in range(1, 46)]  # Genera Store_1 hasta Store_45
    # Eliminar columnas que ya no son necesarias
    datos_entrada.drop(['Store', 'Date'], axis=1, inplace=True)

# Insertar las columnas de tiendas en la posición correcta
posicion_insercion = 1  # Después de 'IsHoliday_True'
for columna in columnas_tiendas:
    columnas_modelo.insert(posicion_insercion, columna)
    posicion_insercion += 1
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

input = datos_entrada[columnas_modelo]
    # Insertar las columnas de tiendas en la posición correcta
    posicion_insercion = 1  # Después de 'IsHoliday_True'
    for columna in columnas_tiendas:
        columnas_modelo.insert(posicion_insercion, columna)
        posicion_insercion += 1

Prediccion = model.predict(input)
Prediccion_str = str(Prediccion).strip('[]')
    input = datos_entrada[columnas_modelo]

Prediccion_str_con_separador = "{:,}".format(float(Prediccion_str))
print("Las ventas para las condiciones especificadas serán: ${} dólares".format(Prediccion_str_con_separador))
    # Realizar la predicción aquí utilizando los datos ingresados en 'datos_entrada'
    # Puedes agregar el código de predicción en esta sección
    Prediccion = run_model_py.model.predict(input)
    Prediccion_str = str(Prediccion).strip('[]')

    # Mostrar la predicción o resultado en Streamlit
    # Por ejemplo, puedes imprimir la predicción en la interfaz
    Prediccion_str_con_separador = "{:,}".format(float(Prediccion_str))
    st.write("Resultado de la predicción:")
    st.write("Las ventas para las condiciones especificadas serán: ${} dólares".format(Prediccion_str_con_separador))
