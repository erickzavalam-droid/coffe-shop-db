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

#Extract
cursor.execute("""SELECT product_type_id, product_type, product_category 
               FROM public.product_type;
               """)
               
tipos_productos = cursor.fetchall()
print(f"Se extrajeron {len(tipos_productos)} registros de tipos de productos.")


for tipo_producto in tipos_productos:
    product_type_id, product_type, product_category = tipo_producto


    cursor.execute("""
        INSERT INTO staging.product_type_staging
            (product_type_id, product_type, product_category)
        VALUES (%s, %s, %s)
        ON CONFLICT (product_type_id) DO UPDATE SET
            product_category = EXCLUDED.product_category,
            loaded_at = NOW();
    """, (product_type_id, product_type, product_category))

connection.commit()
print("Carga a staging.product_type completada.")

cursor.close()
connection.close()

