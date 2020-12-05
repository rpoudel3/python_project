from tkinter import *
import sqlite3


m = Tk()
m.title('Patient Database')
m.geometry("500x400")

conn = sqlite3.connect('patient.db',timeout=10)

cur = conn.cursor()

def add_patient_table(cur):
    cur.execute('DROP TABLE IF EXISTS VITALS')


    # create the table
    cur.execute('''CREATE TABLE VITALS(patient_id INTEGER PRIMARY KEY,
                                         age TEXT,                                                                                       
                                         gender TEXT)''')


# create the employee contacts table
add_patient_table(cur)


