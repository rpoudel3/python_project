from tkinter import *
import sqlite3
import tkinter
import pickle
import pandas as pd

m = Tk()
m.title('Patient Database')
m.geometry("500x400")

conn = sqlite3.connect('patient.db',timeout=10)

cur = conn.cursor()

patient_id = Entry(m, width=30)
patient_id.grid(row=4, column=1)
patientIdLab = Label(m, text="PATIENT ID")
patientIdLab.grid(row=4, column=0)

patient_age = Entry(m, width=30)
patient_age.grid(row=5, column=1)
ageLab = Label(m, text="Age")
ageLab.grid(row=5, column=0)

patient_gender = Entry(m, width=30)
patient_gender.grid(row=6, column=1)
genderLab = Label(m, text="Gender")
genderLab.grid(row=6, column=0)

def add_patient_table(cur):
    cur.execute('DROP TABLE IF EXISTS VITALS')


    # create the table
    cur.execute('''CREATE TABLE VITALS(patient_id INTEGER PRIMARY KEY,
                                         age TEXT,                                                                                       
                                         gender TEXT)''')


# create the employee contacts table
add_patient_table(cur)

def submit():
    conn = sqlite3.connect('patient.db')
    cur = conn.cursor()

    # get all employee contact info
    id = int(patient_id.get())
    age = int(patient_age.get())
    gender = patient_gender.get()

    cur.execute("INSERT OR IGNORE INTO VITALS(PATIENT_ID,AGE,GENDER) VALUES(?, ?, ?)", (id,age,gender))
    conn.commit()
    conn.close()
    # age.delete(0, END)
    # gender.delete(0, END)
    # id.delete(0,END)

def preprocessing_data(test_data):
    gender_map={"M": 1, "F": 0}
    test_data['gender_num'] = test_data['gender'].map(gender_map)
    test_input = test_data[['age', 'gender_num']]
    return test_input

def generate_diabetes_risk_score(test_data):
    filename = 'finalized_model.sav'
    loaded_model = pickle.load(open(filename, 'rb'))
    test_data=preprocessing_data(test_data)
    y_pred_test = loaded_model.predict_proba(test_data)
    print(y_pred_test)
    return y_pred_test[0][0]

def predict_risk():
    conn = sqlite3.connect('patient.db')
    id = int(patient_id.get())
    patient_df = pd.read_sql_query(f"SELECT gender,age FROM VITALS where patient_id={id}", conn)
    risk_score=generate_diabetes_risk_score(patient_df)
    queryM = Label(m)
    queryM.config(text='Probability of diabetes risk score is ' + str(risk_score))
    queryM.grid(row=11, column=0, columnspan=2)
    conn.commit()
    conn.close()

# create Text boxes for both tables

submitB = Button(m, text="Add a Record to the Database", command=submit)
submitB.grid(row=8, column=0, columnspan=2, padx=10, pady=10, ipadx=100)

queryB1 = Button(m, text="Show Prediction", command=lambda: predict_risk())
queryB1.grid(row=9, column=0, columnspan=2, padx=10, pady=10, ipadx=100)

tkinter.mainloop()


