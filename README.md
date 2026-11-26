# 📉 Telco Customer Churn Pipeline: End-to-End ML Data Engineering

## 📌 The Business Problem
Customer retention is the most critical metric for a telecommunications company. It costs significantly more to acquire a new customer than to retain an existing one.

**The Goal:** Build an automated, end-to-end data pipeline that ingests raw customer data into a relational database, engineers features, and trains a machine learning model to predict customer churn before it happens.

## 🔁 What it does
1. **Ingest:** `src/main.py` reads `WA_Fn-UseC_-Telco-Customer-Churn.csv`, cleans it, and loads it into MariaDB.
2. **Store:** 3 normalized tables — Customers, Services, Billing — linked by `customerID`.
3. **Train:** `src/features.py` pulls the data back with a SQL JOIN, engineers features, and trains a Logistic Regression model.
4. **Predict:** `src/batch_predict.py` scores all customers and writes `high_risk.csv` with customers over 65% churn risk.

## 🏗️ Architecture & Tech Stack
- **Database Layer:** MariaDB (relational schema, ACID transactions, FK Cascades)
- **Data Ingestion:** Python, SQLAlchemy, PyMySQL
- **Feature Engineering:** Pandas, One-Hot Encoding, Min-Max Scaling
- **Machine Learning:** Scikit-Learn (Logistic Regression, class-weight balancing)
- **Model Serialization:** Joblib

## 📁 Project Structure
```text
telco-customer-churn/
├── sql/
│   ├── schema.sql            # CREATE TABLE for Customers, Services, Billing
│   └── extract_data.sql      # JOIN Customers + Services + Billing
├── src/
│   ├── main.py               # Phase 1: CSV ingestion to MariaDB
│   ├── preprocessing.py      # Shared preprocessing used by training and prediction
│   ├── features.py           # Phase 2 & 3: Preprocessing & model training
│   └── batch_predict.py      # Phase 4: Score all customers -> high_risk.csv
├── requirements.txt          # Python dependencies
└── README.md                 # Project documentation
```

Files that are generated locally and **not** in this repo (gitignored): the raw CSV, `.env`, `churn_model.joblib`, `churn_scaler.joblib`, `churn_features.joblib`, `high_risk.csv`. Copy `.env.example` to `.env` and fill in your values.

## 🗃️ The tables — what I did
The flat CSV was split by `customerID` into 3 tables in `src/main.py`:

**Customers** — who the customer is
- `customerID VARCHAR(10) PRIMARY KEY`, `gender`, `SeniorCitizen`, `Partner`, `Dependents`

**Services** — what they subscribe to
- `customerID VARCHAR(10) PRIMARY KEY, FOREIGN KEY -> Customers(customerID) ON DELETE CASCADE`
- `PhoneService`, `MultipleLines`, `InternetService`, `OnlineSecurity`, `OnlineBackup`, `DeviceProtection`, `TechSupport`, `StreamingTV`, `StreamingMovies`

**Billing** — contract and charges
- `customerID VARCHAR(10) PRIMARY KEY, FOREIGN KEY -> Customers(customerID) ON DELETE CASCADE`
- `Contract`, `PaperlessBilling`, `PaymentMethod`, `tenure`, `MonthlyCharges`, `TotalCharges`, `Churn`

Cleaning in `main.py`: `TotalCharges` is converted to numeric (blank values become `0.0`), and `Churn` is mapped `Yes -> 1`, `No -> 0` before insert.

To get the data back for training, `sql/extract_data.sql` does:
```sql
SELECT *
FROM Customers
JOIN Services USING (customerID)
JOIN Billing USING (customerID);
```

## 🚀 How to run
Prerequisites: Python >= 3.11, MariaDB running, and the CSV file `WA_Fn-UseC_-Telco-Customer-Churn.csv` in the project root.

1. Create the database and tables:
```bash
mysql -u <user> -p <database_name> < sql/schema.sql
```

2. Copy `.env.example` to `.env` and fill in your values:
```text
USER_DB=<mariadb_user>
DB_PASSWORD=<redacted>
DB_HOST=localhost
DB_NAME=<database_name>
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Load the CSV into MariaDB (run once, on empty tables — `main.py` uses `if_exists='append'`, so running it twice duplicates rows):
```bash
python src/main.py
```

5. Train the model:
```bash
python src/features.py
```

6. Score all customers:
```bash
python src/batch_predict.py
```
This writes `high_risk.csv` with `customerID` and `Risk_Percentage`, sorted by risk, for customers over 65%.

## 📊 Results

Logistic Regression (max_iter=1000, class_weight='balanced'), 20% test split (1,409 customers, random_state=42, stratify=y).

- **Accuracy: 0.738 (73.8%)**
- **Confusion matrix:** [[747, 288], [81, 293]]
- No churn (0): precision 0.90, recall 0.72, F1 0.80 (support 1035)
- Churn (1): precision 0.50, recall 0.78, F1 0.61 (support 374)

Top features: TotalCharges (1.09), Contract_Month-to-month (0.73), InternetService_Fiber optic (0.47). Bottom: tenure (-2.82), Contract_Two year (-0.72).
