import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()


def load_and_clean():
    db = pd.read_csv("WA_Fn-UseC_-Telco-Customer-Churn.csv")
    db['TotalCharges'] = pd.to_numeric(db['TotalCharges'], errors="coerce")
    db['TotalCharges'] = db['TotalCharges'].fillna(0.0)
    db['Churn'] = db['Churn'].map({'Yes': 1, 'No': 0})
    return db


def split_tables(db):
    Customer = db[["customerID", "gender", "SeniorCitizen", "Partner", "Dependents"]].copy()
    Services = db[["customerID", "PhoneService", "MultipleLines", "InternetService", "OnlineSecurity", "OnlineBackup", "DeviceProtection", "TechSupport", "StreamingTV", "StreamingMovies"]].copy()
    Billing = db[["customerID", "Contract", "PaperlessBilling", "PaymentMethod", "tenure", "MonthlyCharges", "TotalCharges", "Churn"]].copy()
    return Customer, Services, Billing


def load_to_db(Customer, Services, Billing):
    url = f"mysql+pymysql://{os.getenv('USER_DB')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:3306/{os.getenv('DB_NAME')}"
    Engine = create_engine(url)

    with Engine.begin() as connection:
        connection.execute(text("DELETE FROM Billing"))
        connection.execute(text("DELETE FROM Services"))
        connection.execute(text("DELETE FROM Customers"))

        Customer.to_sql(name="Customers", con=connection, if_exists='append', index=False)
        Services.to_sql(name="Services", con=connection, if_exists='append', index=False)
        Billing.to_sql(name="Billing", con=connection, if_exists='append', index=False)


def main():
    db = load_and_clean()
    Customer, Services, Billing = split_tables(db)
    load_to_db(Customer, Services, Billing)


if __name__ == "__main__":
    main()