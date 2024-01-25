import altair as alt
import numpy as np
import pandas as pd
import streamlit as st
import pickle
import matplotlib.pyplot as plt

st.title("Welcome again!")

st.markdown("<p style='text-align:center; font-size:24px; font-weight:bold;'>First of all, we provide you with some reference values.</p>", unsafe_allow_html=True)
st.markdown('<p style="font-size:24px; color:#3366ff;">Average predictions for the next 30 days:</p>', unsafe_allow_html=True)
st.markdown('<p style="font-size:20px; color:#ff6600;">Temperature: 58 degrees</p>', unsafe_allow_html=True)
st.markdown('<p style="font-size:20px; color:#ff6600;">Fuel Price: 3.1 dollars per gallon</p>', unsafe_allow_html=True)
st.markdown('<p style="font-size:20px; color:#ff6600;">CPI: 183 base points</p>', unsafe_allow_html=True)
st.markdown('<p style="font-size:20px; color:#ff6600;">Unemployment: 7.1%</p>', unsafe_allow_html=True)


st.markdown("<p style='text-align:center; font-size:24px; font-weight:bold;'>Enter Data for Prediction and enjoy the Magic!</p>", unsafe_allow_html=True)
# Crear campos de entrada para los datos
Temperature = st.slider("Temperature", min_value=0, max_value=100, value=58)
Fuel_Price = st.number_input("Fuel Price", value=3.1)
CPI = st.number_input("CPI(consumer price index", value=183.0)
Unemployment = st.number_input("Unemployment Rate", value=7.1)
#Size = st.number_input("Tamaño de la Tienda", min_value=0)
Store = st.number_input("Store Code (between 1 y 45)", min_value=1, max_value=45)
Date = st.date_input("Date")
IsHoliday_True = st.checkbox("Is it a holiday?")
# Botón para realizar la predicción
if st.button("Let´s Predict"):
    # Crear un DataFrame con los datos ingresados

    datos_entrada = pd.DataFrame([{
        'Temperature': Temperature,
        'Fuel_Price': Fuel_Price,
        'CPI': CPI,
        'Unemployment': Unemployment,
        'Size': 200898,
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
    try:
        model = pickle.load(open('model.pkl', 'rb'))
    except Exception as e:
        st.error(f"Error al cargar el modelo: {e}")
        model = None  # Asegura que el modelo es None si falla la carga

    #Prediccion = run_model_py.model.predict(input)
    
    Prediccion = model.predict(input)
    Prediccion_str = str(Prediccion).strip('[]')

    #st.text(Prediccion)
    Prediccion_str_con_separador = "{:,}".format(float(Prediccion_str))
    st.write("Resultado de la predicción:")
    st.write("Las ventas para las condiciones especificadas serán: ${} dólares".format(Prediccion_str_con_separador))

    output = pd.read_excel('output.xlsx', index_col=0)
    
    store_number = int(Store)
    
    # Assuming 'df' is your DataFrame
    # Filter data for Store 1
    if store_number != 0:
        store_1_data = output[output['Store'] == int(store_number)]
    
        title = f'Weekly Sales and Predicted Sales for Store {store_number}'
    
    else:
        store_1_data = pd.DataFrame(output.groupby('Date').sum().reset_index(drop = False))
        Pred_sales = []
        contador = 0
        for i in store_1_data['Pred_sales']:
            if i == 0:
                Pred_sales.append(None)
    
            elif contador ==0:
                Pred_sales.append(None)
                contador += 1
    
            else:
    
                Pred_sales.append(i)
                contador+=1
    
        store_1_data['Pred_sales'] = Pred_sales
        store_1_data = store_1_data[1:]
    
        title = 'Weekly Sales and Predicted Sales for all stores'
    
    # Convert 'Date' column to datetime
    store_1_data['Date'] = pd.to_datetime(store_1_data['Date'])
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(store_1_data['Date'].values, store_1_data['Weekly_Sales'].values, label='Weekly Sales')
    ax.plot(store_1_data['Date'].values, store_1_data['Pred_sales'].values, label='Pred_sales', linestyle='--', color='orange')
    
    # Personalizar el gráfico
    ax.set_title("Weekly Sales Evolution")
    ax.set_xlabel('Date')
    ax.set_ylabel('Sales')
    ax.legend()
    
    # Mostrar el gráfico en Streamlit
    st.pyplot(fig)
