# -*- coding: utf-8 -*-
import psycopg2
import os
from dotenv import load_dotenv
from datetime import date

load_dotenv()

#Connection
start = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
    )

cursor = start.cursor()

#Extract
cursor.execute("""SELECT customer_id, customer_name, email, reg_date, 
               card_number, date_of_birth, gender
               FROM public.customer;
               """)
               
clientes = cursor.fetchall()
print(f"Se extrajeron {len(clientes)} registros de customer.")

#Transform
hoy = date.today()

for cliente in clientes:
    customer_id, customer_name, email, reg_date, card_number, date_of_birth, gender = cliente
    
    
    if date_of_birth is None:
        continue
    
   
    edad = hoy.year - date_of_birth.year - (
        (hoy.month, hoy.day) < (date_of_birth.month, date_of_birth.day)
        )
    
    cursor.execute("""
        INSERT INTO staging.customer_staging
            (customer_id, customer_name, email, reg_date,
             card_number, date_of_birth, gender, age)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (customer_id) DO NOTHING;
    """, (customer_id, customer_name, email, reg_date,
          card_number, date_of_birth, gender, edad))

start.commit()
print("Carga a staging.customer_staging completada.")

cursor.close()
start.close()

