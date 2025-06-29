import mysql.connector
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

def get_connected():
    return mysql.connector.connect(
        host = st.secrets["DB_HOST"],
        user = st.secrets["DB_USER"],
        password = st.secrets["DB_PASSWORD"],
        database = st.secrets["DB_NAME"]
    )

def save_simulation(inputs, output_matrix):
    conn = get_connected()
    cursor = conn.cursor()

    insert_inputs = """
        INSERT INTO BlackScholesInputs 
        (StockPrice, StrikePrice, InterestRate, Volatility, TimeToExpiry, CallPurchasePrice, PutPurchasePrice)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    input_values = (
        inputs['StockPrice'],
        inputs['StrikePrice'],
        inputs['InterestRate'],
        inputs['Volatility'],
        inputs['TimeToExpiry'],
        inputs['CallPurchasePrice'],
        inputs['PutPurchasePrice']
    )

    cursor.execute(insert_inputs, input_values)
    input_id = cursor.lastrowid

    insert_output = """
        INSERT INTO BlackScholesOutputs 
        (VolatilityShock, StockPriceShock, OptionPrice, IsCall, CalculationId)
        VALUES (%s, %s, %s, %s, %s)
    """

    for row in output_matrix:
        cursor.execute(insert_output, (
            row['vol'],
            row['spot'],
            row['price'],
            row['is_call'],
            calc_id := input_id
        ))

    conn.commit()
    cursor.close()
    conn.close()

    