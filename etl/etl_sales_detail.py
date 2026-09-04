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

#Watermark
cursor.execute("SELECT COALESCE(MAX(sales_detail_id), 0) FROM staging.sales_detail_staging;")
last_id = cursor.fetchone()[0]
print(f"Último sales_detail_id cargado en staging: {last_id}")

#Extract
cursor.execute("""
    SELECT sales_detail_id, transaction_id, product_id, quantity, price
    FROM public.sales_detail
    WHERE sales_detail_id > %s;
    """, (last_id,))
               
detalle_ventas = cursor.fetchall()
print(f"Se extrajeron {len(detalle_ventas)} registros de sales_detail.")


for detalle_venta in detalle_ventas:
    sales_detail_id, transaction_id, product_id, quantity, price = detalle_venta

    subtotal = quantity * price
    
    cursor.execute("""
        INSERT INTO staging.sales_detail_staging
            (sales_detail_id, transaction_id, product_id, quantity, price, subtotal)
        VALUES (%s, %s, %s, %s, %s, %s);
    """, (sales_detail_id, transaction_id, product_id, quantity, price, subtotal))

connection.commit()
print("Carga a staging.sales_detail_staging completada.")

cursor.close()
connection.close()


