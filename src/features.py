import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib

load_dotenv()

url=f"mysql+pymysql://{os.getenv('USER_DB')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:3306/{os.getenv('DB_NAME')}"
engine=create_engine(url)

with open("sql/extract_data.sql",'r') as f:
    query = f.read()

## Extraction :

try:
    db=pd.read_sql(query, con=engine)
    print("Data succesfully extracted !")
    db = db.drop('customerID',axis=1)
    print(f"Columns : {db.columns}")
except Exception as e:
    print(f"Error Occured: {e}")

## Gender to binary :

db['gender']=db['gender'].map({'Male':0,'Female':1})

## Yes/No's to binary : 

YNCOLUMNS = ['Partner','Dependents','PhoneService','PaperlessBilling']
for c in YNCOLUMNS :
    try:
        db[c]=db[c].map({'Yes':1,'No':0})
    except Exception as e:
        print(f"Error : {e}")


print(db.head())

## Multi Cols :

mc = ['MultipleLines', 'InternetService', 'OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies', 'Contract', 'PaymentMethod']
db= pd.get_dummies(db,columns=mc,dtype=int)

## Scaling : 

num_cols = ['tenure', 'MonthlyCharges', 'TotalCharges']
scaler= MinMaxScaler()

db[num_cols]=scaler.fit_transform(db[num_cols])

print(f"Columns : {db.columns}")

## Evaluation :
X = db.drop('Churn',axis=1)
y = db['Churn']

X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2,train_size=0.8,random_state=42)

## Training :

model = LogisticRegression(max_iter=1000,class_weight='balanced')
model.fit(X_train,y_train)

## Accuracy_Score : 

predictions = model.predict(X_test)
accuracy = accuracy_score(y_test,predictions)
print(f"Model accuracy = {accuracy}")
print(f"Confusion matrix : {confusion_matrix(y_test,predictions)}")
print(f"Report : {classification_report(y_test,predictions)}")

## Importance coefficients :

features = X.columns
weights = model.coef_[0]

importance_df = pd.DataFrame({
    "Feature" : features,
    "Weight" : weights
})
importance_df=importance_df.sort_values(by='Weight',ascending=False)
print(importance_df.head())
print(importance_df.tail())
## Saving the model and the scaler :
joblib.dump(model, 'churn_model.joblib')
joblib.dump(scaler, 'churn_scaler.joblib')