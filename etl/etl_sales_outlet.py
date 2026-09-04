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
cursor.execute("""SELECT sales_outlet_id, sales_outlet_type, address, city, telephone, postal_code, manager   
               FROM public.sales_outlet;
               """)
               
punto_ventas = cursor.fetchall()
print(f"Se extrajeron {len(punto_ventas)} registros de sales_outlet.")


for punto_venta in punto_ventas:
    sales_outlet_id, sales_outlet_type, address, city, telephone, postal_code, manager = punto_venta
    
    cursor.execute("""
        INSERT INTO staging.sales_outlet_staging
            (sales_outlet_id, sales_outlet_type, address, city, telephone, postal_code, manager)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (sales_outlet_id) DO UPDATE SET
            telephone = EXCLUDED.telephone,
            manager = EXCLUDED.manager,
            loaded_at = NOW();
    """, (sales_outlet_id, sales_outlet_type, address, city, telephone, postal_code, manager))
    
connection.commit()
print("Carga a staging.sales_outlet_staging completada.")

cursor.close()
connection.close()




