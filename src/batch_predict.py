import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import joblib
load_dotenv()

url=f"mysql+pymysql://{os.getenv('USER_DB')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:3306/{os.getenv('DB_NAME')}"
engine = create_engine(url)

with open("sql/extract_data.sql",'r') as f:
    query = f.read()

try:
    db=pd.read_sql(query, con=engine)
    print("Data extracted!")
    customersIDs=db['customerID']
    db=db.drop('customerID',axis=1)
except Exception as e:
    print(f"Error : {e}")

## Binaries : 

db['gender']=db['gender'].map({'Male': 0, 'Female': 1})

yncolumns = ['Partner','Dependents','PhoneService','PaperlessBilling']

for c in yncolumns:
    db[c]=db[c].map({'Yes': 1, 'No': 0})

mc = ['MultipleLines', 'InternetService', 'OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies', 'Contract', 'PaymentMethod']
db=pd.get_dummies(db,columns=mc,dtype=int)

## Scaler

X=db.drop('Churn',axis=1)

scaler= joblib.load('churn_scaler.joblib')

num_cols = ['tenure', 'MonthlyCharges', 'TotalCharges']

X[num_cols]=scaler.transform(X[num_cols])

## Model

model= joblib.load('churn_model.joblib')

churn_risk= model.predict_proba(X)[:,1]

## The final report

report = pd.DataFrame({
    'customerID': customersIDs,
    'Risk_Percentage': (churn_risk*100).round(2)
})

High_risk = report[report['Risk_Percentage'] > 65.0].sort_values(by='Risk_Percentage',ascending=False)
High_risk.to_csv('high_risk.csv',index=False)