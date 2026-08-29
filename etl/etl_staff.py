# -*- coding: utf-8 -*-
import psycopg2
import os 
from dotenv import load_dotenv
from datetime import date

load_dotenv()
#Connection
connection = psycopg2.connect(
    host =os.getenv("DB_HOST"),
    port =os.getenv("DB_PORT"),
    dbname =os.getenv("DB_NAME"),
    user =os.getenv("DB_USER"),
    password =os.getenv("DB_PASSWORD")
    )

cursor = connection.cursor()

#Extract

cursor.execute("""SELECT staff_id, first_name, last_name, position, start_date, location
               FROM public.staff;""")
               
employees = cursor.fetchall()
print(f"Se extrajeron {len(employees)} registros de staff.")

#Transform
now = date.today()

for employee in employees:
    staff_id, first_name, last_name, position, start_date, location = employee
    
    if start_date is None: 
        continue
    
    time_service = now.year - start_date.year - (
        (now.month, now.day) < (start_date.month, start_date.day)
        )
    
    cursor.execute ("""
        INSERT INTO staging.staff_staging
            (staff_id, first_name, last_name, position_work, start_date,
            years_service, work_location)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (staff_id) DO UPDATE SET
            position_work = EXCLUDED.position_work,
            years_service = EXCLUDED.years_service,
            work_location = EXCLUDED.work_location,
            loaded_at = now();
    """, (staff_id, first_name, last_name, position, start_date, time_service, location))
    
connection.commit()
print("Carga a prueba.staff_table completada.")

cursor.close()
connection.close()
                   
                       
                     