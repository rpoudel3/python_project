import sklearn
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics
import pickle


data = {'age': [30, 60, 65, 66],'gender': ['F', 'M', 'M', 'M'], 'diabetes': [0, 1, 1, 1]}
train_data=pd.DataFrame.from_dict(data)

print(train_data)

gender_map = {"M" : 1, "F" : 0}
train_data['gender_num'] = train_data['gender'].map(gender_map)

X=train_data[['age', 'gender_num']]  # Features
y=train_data['diabetes']  # Labels

# train the model
model=RandomForestClassifier()
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3) # 70% training and 30% test

model.fit(X_train,y_train)

y_pred=model.predict(X_test)

print(X_test)
print("Accuracy:",metrics.accuracy_score(y_test, y_pred))

# save the model
filename = 'finalized_model.sav'
pickle.dump(model, open(filename, 'wb'))

#preprocessing and test data
data_2 = {'age': [22],'gender': ['M']}
test_data=pd.DataFrame.from_dict(data_2)
gender_map = {"M" : 1, "F" : 0}
test_data['gender_num'] = test_data['gender'].map(gender_map)
test_input=test_data[['age', 'gender_num']]  # Features


# load the model from disk
filename = 'finalized_model.sav'
loaded_model = pickle.load(open(filename, 'rb'))
y_pred_test=loaded_model.predict_proba(test_input)
print(y_pred_test[0][0])


def gender_map():
    return {"M" : 1, "F" : 0}

def preprocessing_data(test_data):
    test_data['gender_num'] = test_data['gender'].map(gender_map)
    test_input = test_data[['age', 'gender_num']]
    return test_input

def predict_diabetes_risk_score(test_data):
    filename = 'finalized_model.sav'
    loaded_model = pickle.load(open(filename, 'rb'))
    y_pred_test = loaded_model.predict_proba(test_data)
    return y_pred_test[0][0]

