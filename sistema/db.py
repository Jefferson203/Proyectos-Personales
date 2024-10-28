import psycopg2

DB_HOST = "localhost"
DB_NAME = "sistemaAsistencia"
DB_USER = "postgres"
DB_PASS = "76729987"
 
conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
