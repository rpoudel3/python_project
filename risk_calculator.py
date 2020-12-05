from tkinter import *
import sqlite3
import tkinter
import pickle
import pandas as pd


class RiskCalculator:
    def __init__(self):
        self.m = Tk()
        self.m.title('Patient Database')
        self.m.geometry("500x400")

        self.conn = sqlite3.connect('patient.db',timeout=30)

        self.cur = self.conn.cursor()

        self.patient_id = Entry(self.m, width=30)
        self.patient_id.grid(row=4, column=1)
        self.patientIdLab = Label(self.m, text="PATIENT ID")
        self.patientIdLab.grid(row=4, column=0)

        self.patient_age = Entry(self.m, width=30)
        self.patient_age.grid(row=5, column=1)
        self.ageLab = Label(self.m, text="Age")
        self.ageLab.grid(row=5, column=0)

        self.patient_gender = Entry(self.m, width=30)
        self.patient_gender.grid(row=6, column=1)
        self.genderLab = Label(self.m, text="Gender")
        self.genderLab.grid(row=6, column=0)

        # create Text boxes for both tables
        self.submitB = Button(self.m, text="Add a Record to the Database", command=self.submit)
        self.submitB.grid(row=8, column=0, columnspan=2, padx=10, pady=10, ipadx=100)

        self.queryB1 = Button(self.m, text="Show Prediction", command=lambda: self.predict_risk())
        self.queryB1.grid(row=9, column=0, columnspan=2, padx=10, pady=10, ipadx=100)

        tkinter.mainloop()

    def add_patient_table(self):
        self.cur.execute('DROP TABLE IF EXISTS VITALS')


        # create the table
        self.cur.execute('''CREATE TABLE VITALS(patient_id INTEGER PRIMARY KEY,
                                             age TEXT,                                                                                       
                                             gender TEXT)''')

    def submit(self):
        # create the employee contacts table
        self.add_patient_table()

        # get all employee contact info
        id = int(self.patient_id.get())
        age = int(self.patient_age.get())
        gender = self.patient_gender.get()

        self.cur.execute("INSERT OR IGNORE INTO VITALS(PATIENT_ID,AGE,GENDER) VALUES(?, ?, ?)", (id,age,gender))

    def preprocessing_data(self,test_data):
        gender_map={"M": 1, "F": 0}
        test_data['gender_num'] = test_data['gender'].map(gender_map)
        test_input = test_data[['age', 'gender_num']]
        return test_input

    def generate_diabetes_risk_score(self,test_data):
        filename = 'finalized_model.sav'
        loaded_model = pickle.load(open(filename, 'rb'))
        test_data=self.preprocessing_data(test_data)
        y_pred_test = loaded_model.predict_proba(test_data)
        print(y_pred_test)
        return y_pred_test[0][0]

    def predict_risk(self):
        id = int(self.patient_id.get())
        patient_df = pd.read_sql_query(f"SELECT gender,age FROM VITALS where patient_id={id}", self.conn)
        risk_score=self.generate_diabetes_risk_score(patient_df)
        queryM = Label(self.m)
        queryM.config(text='Probability of diabetes risk score is ' + str(risk_score))
        queryM.grid(row=11, column=0, columnspan=2)
        self.conn.commit()
        self.conn.close()


if __name__=='__main__':
    RiskCalculator()
