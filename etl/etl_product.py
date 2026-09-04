# -*- coding: utf-8 -*-
import psycopg2
import os 
from dotenv import load_dotenv

load_dotenv()

connection = psycopg2.connect(
    host =os.getenv("DB_HOST"),
    port =os.getenv("DB_PORT"),
    dbname =os.getenv("DB_NAME"),
    user =os.getenv("DB_USER"),
    password =os.getenv("DB_PASSWORD")
    )

cursor = connection.cursor()

cursor.execute("""SELECT product_id, product_name, description, 
               product_price, product_type_id FROM public.product;""")
               
productos = cursor.fetchall()
print(f"Se extrajeron {len(productos)} registros de product")

for producto in productos:
    product_id, product_name, description, product_price, product_type_id = producto
    

    cursor.execute("""
        INSERT INTO staging.product_staging 
            (product_id, product_name, description, product_price, product_type_id)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (product_id) DO UPDATE SET
            product_price = EXCLUDED.product_price,
            loaded_at = NOW();
    """, (product_id, product_name, description, product_price, product_type_id))
    
connection.commit()
print("Carga a staging.product_staging ha sido exitosa.")

cursor.close()
connection.close()