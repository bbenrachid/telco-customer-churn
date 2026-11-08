-- Main tables : Customers
CREATE TABLE Customers (
    customerID VARCHAR(10) PRIMARY KEY,
    gender VARCHAR(10),
    SeniorCitizen TINYINT(1),
    Partner VARCHAR(5),
    Dependents VARCHAR(5)
) ENGINE=InnoDB;

-- Dependent tables : Services
CREATE TABLE Services (
    customerID VARCHAR(10) PRIMARY KEY,
    PhoneService VARCHAR(5),
    MultipleLines VARCHAR(20),
    InternetService VARCHAR(20),
    OnlineSecurity VARCHAR(25),
    OnlineBackup VARCHAR(25),
    DeviceProtection VARCHAR(25),
    TechSupport VARCHAR(25),
    StreamingTV VARCHAR(25),
    StreamingMovies VARCHAR(25),
    CONSTRAINT fk_srv_cust FOREIGN KEY (customerID)
    REFERENCES Customers(customerID)
    ON DELETE CASCADE
) ENGINE=InnoDB;

-- Dependent table : Facturation
CREATE TABLE Billing (
    customerID VARCHAR(10) PRIMARY KEY,
    Contract VARCHAR(20),
    PaperlessBilling VARCHAR(5),
    PaymentMethod VARCHAR(30),
    tenure INT,
    MonthlyCharges DECIMAL(10, 2),
    TotalCharges DECIMAL(10, 2) NULL,
    Churn VARCHAR(5),
    CONSTRAINT fk_bill_custid FOREIGN KEY (customerID)
    REFERENCES Customers(customerID)
    ON DELETE CASCADE
) ENGINE=InnoDB;