# 📉 Telco Customer Churn Pipeline: End-to-End ML Data Engineering

## 📌 The Business Problem
Customer retention is the most critical metric for a telecommunications company. It costs significantly more to acquire a new customer than to retain an existing one. 

**The Goal:** Build an automated, end-to-end data pipeline that ingests raw customer data into a relational database, engineers features, and trains a machine learning model to predict customer churn before it happens.

## 🏗️ Architecture & Tech Stack
- **Database Layer:** MariaDB (Relational schema, ACID transactions, FK Cascades)
- **Data Ingestion:** Python, SQLAlchemy, PyMySQL
- **Feature Engineering:** Pandas, One-Hot Encoding, Min-Max Scaling
- **Machine Learning:** Scikit-Learn (Logistic Regression, class-weight balancing)
- **Model Serialization:** Joblib

## 📁 Project Structure
```text
telco-customer-churn/
├── sql/
│   └── extract_data.sql      # Modular extraction queries
├── src/
│   ├── main.py               # Phase 1: CSV Ingestion to MariaDB
│   └── features.py           # Phase 2 & 3: Preprocessing & Model Training
├── churn_model.joblib        # Serialized ML model
├── churn_scaler.joblib       # Serialized Min-Max Scaler
├── .env.example              # Template for DB credentials
├── requirements.txt          # Python dependencies
└── README.md                 # Project documentation