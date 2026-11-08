import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

url=f"mysql+pymysql://{os.getenv('USER_DB')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:3306/{os.getenv('DB_NAME')}"
engine=create_engine(url)

with open("sql/extract_data.sql",'r') as f:
    query = f.read()

try:
    db=pd.read_sql(query, con=engine)
    print("Data succesfully extracted !")
    print(db.head())
    print(f"Shape : {db.shape}")
    print(db.info())
except Exception as e:
    print(f"Error Occured: {e}")