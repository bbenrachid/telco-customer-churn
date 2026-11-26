import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import joblib
from preprocessing import preprocess
from pathlib import Path
load_dotenv()
ROOT = Path(__file__).resolve().parent.parent
SQL_PATH = ROOT / "sql" / "extract_data.sql"
MODEL_PATH = ROOT / "churn_model.joblib"
SCALER_PATH = ROOT / "churn_scaler.joblib"
CHURN_FEATURES = ROOT / "churn_features.joblib"
REPORT = ROOT / "high_risk.csv"

url=f"mysql+pymysql://{os.getenv('USER_DB')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:3306/{os.getenv('DB_NAME')}"
engine = create_engine(url)

with open(SQL_PATH,'r') as f:
    query = f.read()


db=pd.read_sql(query, con=engine)
customersIDs=db['customerID']
db=db.drop('customerID',axis=1)

##Saved list
saved_list = joblib.load(CHURN_FEATURES)
X,y=preprocess(db,saved_list)
## Scaler


scaler= joblib.load(SCALER_PATH)

num_cols = ['tenure', 'MonthlyCharges', 'TotalCharges']

X[num_cols]=scaler.transform(X[num_cols])

## Model

model= joblib.load(MODEL_PATH)

churn_risk= model.predict_proba(X)[:,1]

## The final report

report = pd.DataFrame({
    'customerID': customersIDs,
    'Risk_Percentage': (churn_risk*100).round(2)
})

High_risk = report[report['Risk_Percentage'] > 65.0].sort_values(by='Risk_Percentage',ascending=False)
High_risk.to_csv(REPORT,index=False)