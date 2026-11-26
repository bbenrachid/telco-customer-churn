import pandas as pd
YN_COLS = ['Partner', 'Dependents', 'PhoneService', 'PaperlessBilling']
MULTI_COLS = ['MultipleLines', 'InternetService', 'OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies', 'Contract', 'PaymentMethod']
NUM_COLS = ['tenure', 'MonthlyCharges', 'TotalCharges']

def preprocess(df, feature_columns=None):
    df = df.copy()
    df['gender']=df['gender'].map({'Male': 0, 'Female': 1})
    for c in YN_COLS:
        df[c]=df[c].map({'Yes':1,'No':0})
    df=pd.get_dummies(df,columns=MULTI_COLS,dtype=int)

    if 'Churn' in df.columns:
        y= df['Churn']
        X=df.drop('Churn', axis=1)
    else:
        y= None
        X=df

    if feature_columns is not None:
        X = X.reindex(columns=feature_columns, fill_value=0)
    return X,y