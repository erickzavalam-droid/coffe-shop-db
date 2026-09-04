# -*- coding: utf-8 -*-
import psycopg2
import os
from dotenv import load_dotenv


load_dotenv()

#Connection
connection = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
    )

cursor = connection.cursor()

#watermark
cursor.execute("SELECT COALESCE(MAX(transaction_id), 0) FROM staging.sales_transaction_staging;")
               
last_id = cursor.fetchone()[0]
print(f"Último transaction_id cargado en staging: {last_id}")

#Extract
cursor.execute("""
    SELECT transaction_id, transaction_date, transaction_time, sales_outlet_id, staff_id, customer_id
    FROM public.sales_transaction
    WHERE transaction_id > %s;
    """, (last_id,))

transacciones = cursor.fetchall()
print(f"Se extrajeron {len(transacciones)} registros de sales_transaction.")


for transaccion in transacciones:
    transaction_id, transaction_date, transaction_time, sales_outlet_id, staff_id, customer_id = transaccion
    
    cursor.execute("""
        INSERT INTO staging.sales_transaction_staging
            (transaction_id, transaction_date, transaction_time, sales_outlet_id, staff_id, customer_id)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (transaction_id, transaction_date, transaction_time, sales_outlet_id, staff_id, customer_id))
    
connection.commit()
print("Carga a staging.sales_transaction_staging completada.")

cursor.close()
connection.close()

