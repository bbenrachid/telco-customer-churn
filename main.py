import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
load_dotenv()

db=pd.read_csv("WA_Fn-UseC_-Telco-Customer-Churn.csv")
db['TotalCharges']=pd.to_numeric(db['TotalCharges'],errors="coerce")
db['TotalCharges']=db['TotalCharges'].fillna(0.0)
db['Churn']=db['Churn'].map({'Yes':1,'No':0})

Customer=db[["customerID","gender","SeniorCitizen","Partner","Dependents"]].copy()

Services=db[["customerID","PhoneService","MultipleLines","InternetService","OnlineSecurity","OnlineBackup","DeviceProtection","TechSupport","StreamingTV","StreamingMovies"]].copy()

Billing=db[["customerID","Contract","PaperlessBilling","PaymentMethod","tenure","MonthlyCharges","TotalCharges","Churn"]].copy()

url=f"mysql+pymysql://{os.getenv('USER_DB')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:3306/{os.getenv('DB_NAME')}"
Engine= create_engine(url)

with Engine.begin() as connection:

    Customer.to_sql(name="Customers",con=connection,if_exists='append',index=False)

    Services.to_sql(name="Services",con=connection,if_exists='append',index=False)

    Billing.to_sql(name="Billing",con=connection,if_exists='append',index=False)

print(db.dtypes)