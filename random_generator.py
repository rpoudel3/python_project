import numpy as np
import random
rows = []
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics
import pickle

class ModelTrainer():
    def generate_training_data():
        rows = []
        age_range = np.arange(20, 100, 1).tolist()
        gender = ['M', 'F']
        diabetes = [0, 1]

        for x in range(1,50):
            dict_row={"patient_id":x,
                    "gender": random.choice(gender),
                    "diabetes": random.choice(diabetes),
                    "age": np.random.choice(age_range)
                      }
            rows.append(dict_row)
        train_data=pd.DataFrame.from_dict(rows)
        return train_data

    def train_rf_model(train_data):
        gender_map = {"M": 1, "F": 0}
        train_data['gender_num'] = train_data['gender'].map(gender_map)
        X = train_data[['age', 'gender_num']]  # Features
        y = train_data['diabetes']  # Labels

        # train the model
        model = RandomForestClassifier()
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)  # 70% training and 30% test
        model.fit(X_train, y_train)

        # print and show the accuracy of the model
        y_pred = model.predict(X_test)
        print("Accuracy:", metrics.accuracy_score(y_test, y_pred))

        # save the model
        filename = 'finalized_model.sav'
        pickle.dump(model, open(filename, 'wb'))

    train_data=generate_training_data()
    train_rf_model(train_data)

if __name__=='main':
    ModelTrainer()
