import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import datetime
import sys

print("🚀 Starting Enterprise ETL Pipeline...")

# =========================================================
# 1. DATABASE CONNECTION CONFIGURATION

import urllib.parse

DB_USER = "postgres"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "credit_risk_dw"

# 🛑 PUT YOUR EXACT PASSWORD BETWEEN THESE QUOTES ONLY
DB_PASSWORD = "Vvkpragya@22"

# Safe password URL encoding (Handles special characters like @ safely)
safe_password = urllib.parse.quote_plus(DB_PASSWORD)

# Clean connection string builder
connection_string = f"postgresql://{DB_USER}:{safe_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(connection_string)
# =========================================================
# 2. LOAD RAW KAGGLE DATA
# =========================================================
# 🛑 ACTION REQUIRED: Ensure your file is named exactly 'loan_default.csv' in this folder
try:
    df = pd.read_csv("data/raw/Loan_default.csv")
    print(f"✔ Raw dataset loaded successfully: {df.shape[0]} rows found.")
except FileNotFoundError:
    print("❌ Error: 'loan_default.csv' not found inside this folder.")
    print("Please make sure the Kaggle file is renamed and saved in this exact PyCharm project directory.")
    sys.exit()
# ==============================================================================
# ENTERPRISE RISK ENGINE TRANSFORMATIONS (From Data Audit Scripts)
# ==============================================================================

# 1. Income Risk Score (Low Income = High Risk)
df['income_score'] = pd.qcut(df['Income'], q=4, labels=[4, 3, 2, 1]).astype(int)

# 2. Credit Score Risk Band
df['credit_band_score'] = pd.cut(df['CreditScore'], bins=[-1, 500, 600, 700, 1000], labels=[4, 3, 2, 1]).astype(int)

# 3. Employment Risk Score Mapping
employment_map = {'Unemployed': 4, 'Part-time': 3, 'Self-employed': 2, 'Full-time': 1}
df['employment_score'] = df['EmploymentType'].map(employment_map)

# 4. Final Aggregated Risk Score & Category
df['risk_score'] = df['income_score'] + df['credit_band_score'] + df['employment_score']

df['risk_category'] = pd.cut(
    df['risk_score'],
    bins=[0, 4, 7, 9, 12],
    labels=['Low Risk', 'Medium Risk', 'High Risk', 'Very High Risk']
).astype(str)

# Clean up any accidental blank spaces in column headers
df.columns = [col.strip() for col in df.columns]

# Create standard tracking keys across our schema
df['customer_id'] = range(1, len(df) + 1)
if 'LoanID' in df.columns:
    df['loan_id'] = df['LoanID']
else:
    df['loan_id'] = ["LN" + str(x).zfill(8) for x in range(1, len(df) + 1)]

# =========================================================
# 3. EXTRACTION & BULK INSERT INTO DIMENSIONS
# =========================================================
print("⏳ Populating Dimension Tables (Bulk Loading)...")

# Dim Customer
dim_customer = pd.DataFrame({
    'customer_id': df['customer_id'],
    'age': df.get('Age', np.random.randint(21, 65, size=len(df))),
    'marital_status': df.get('MaritalStatus', np.random.choice(['Single', 'Married', 'Divorced'], size=len(df))),
    'has_dependents': df.get('HasDependents', np.random.choice(['Yes', 'No'], size=len(df))),
    'has_mortgage': df.get('HasMortgage', np.random.choice(['Yes', 'No'], size=len(df)))
}).drop_duplicates(subset=['customer_id'])

dim_customer.to_sql('dim_customer', engine, if_exists='append', index=False, chunksize=10000)
print("  ✔ dim_customer loaded.")

# Dim Employment
dim_employment = pd.DataFrame({
    'employment_id': df['customer_id'],
    'employment_type': df.get('EmploymentType', np.random.choice(['Full-time', 'Part-time', 'Self-employed', 'Unemployed'], size=len(df))),
    'months_employed': df.get('MonthsEmployed', np.random.randint(0, 120, size=len(df)))
})
dim_employment['employment_band'] = pd.cut(dim_employment['months_employed'], bins=[-1, 12, 36, 60, 200], labels=['0-1 Year', '1-3 Years', '3-5 Years', '5+ Years'])

dim_employment.to_sql('dim_employment', engine, if_exists='append', index=False, chunksize=10000)
print("  ✔ dim_employment loaded.")

# Dim Education
unique_edu = df['Education'].unique() if 'Education' in df.columns else ['High School', 'Bachelor', 'Master', 'PhD']
dim_education = pd.DataFrame({'education_id': range(1, len(unique_edu)+1), 'education': unique_edu})
dim_education.to_sql('dim_education', engine, if_exists='append', index=False)

edu_map = dict(zip(dim_education['education'], dim_education['education_id']))
df['education_id'] = df['Education'].map(edu_map) if 'Education' in df.columns else np.random.choice(dim_education['education_id'], size=len(df))
print("  ✔ dim_education loaded.")

# Dim Loan Purpose
unique_purp = df['LoanPurpose'].unique() if 'LoanPurpose' in df.columns else ['Home', 'Auto', 'Education', 'Business', 'Personal']
dim_loan_purpose = pd.DataFrame({'purpose_id': range(1, len(unique_purp)+1), 'loan_purpose': unique_purp})
dim_loan_purpose.to_sql('dim_loan_purpose', engine, if_exists='append', index=False)

purp_map = dict(zip(dim_loan_purpose['loan_purpose'], dim_loan_purpose['purpose_id']))
df['purpose_id'] = df['LoanPurpose'].map(purp_map) if 'LoanPurpose' in df.columns else np.random.choice(dim_loan_purpose['purpose_id'], size=len(df))
print("  ✔ dim_loan_purpose loaded.")

# Dim Branch
regions = ['Northeast', 'Southeast', 'Midwest', 'Southwest', 'West']
dim_branch = pd.DataFrame({
    'branch_id': range(1, 101),
    'branch_name': [f"Branch Office {i}" for i in range(1, 101)],
    'city': [f"Metro City {i}" for i in range(1, 101)],
    'state': [f"State {i}" for i in range(1, 101)],
    'region': np.random.choice(regions, size=100)
})
dim_branch.to_sql('dim_branch', engine, if_exists='append', index=False)
print("  ✔ dim_branch loaded.")

# =========================================================
# 4. LOAD CORE FACT TABLE (LOAN PERFORMANCE)
# =========================================================
print("⏳ Populating Central Fact Table (fact_loan_performance)...")

fact_loan = pd.DataFrame({
    'loan_id': df['loan_id'],
    'customer_id': df['customer_id'],
    'employment_id': df['customer_id'],
    'education_id': df['education_id'],
    'purpose_id': df['purpose_id'],
    'loan_amount': df.get('LoanAmount', np.random.uniform(5000, 50000, size=len(df))),
    'interest_rate': df.get('InterestRate', np.random.uniform(3.5, 24.9, size=len(df))),
    'loan_term': df.get('LoanTerm', np.random.choice([12, 24, 36, 48, 60], size=len(df))),
    'credit_score': df.get('CreditScore', np.random.randint(300, 850, size=len(df))),
    'income': df.get('Income', np.random.uniform(20000, 150000, size=len(df))),
    'dti_ratio': df.get('DTIRatio', np.random.uniform(0.1, 0.6, size=len(df))),
    'default_flag': df.get('Default', np.random.choice([0, 1], p=[0.88, 0.12], size=len(df))),
    'risk_score': df['risk_score'],
    'risk_category': df['risk_category']
}).drop_duplicates(subset=['loan_id'])

fact_loan.to_sql('fact_loan_performance', engine, if_exists='append', index=False, chunksize=10000)
print(f"  ✔ fact_loan_performance loaded with {len(fact_loan)} records.")

# =========================================================
# 5. GENERATE HIGH VOLUME TRANSACTIONS: PAYMENT HISTORY
# =========================================================
print("⏳ Synthesizing 1.5 Million+ Amortized Payments (This will take a brief moment)...")

loan_ids = fact_loan['loan_id'].values
terms = fact_loan['loan_term'].values
amounts = fact_loan['loan_amount'].values
defaults = fact_loan['default_flag'].values

max_payments = 6
repeated_loans = np.repeat(loan_ids, max_payments)
repeated_terms = np.repeat(terms, max_payments)
repeated_amounts = np.repeat(amounts, max_payments)
repeated_defaults = np.repeat(defaults, max_payments)
p_idx = np.tile(np.arange(1, max_payments + 1), len(loan_ids))

base_payment_amt = repeated_amounts / repeated_terms
days_late_gen = np.where(repeated_defaults == 1, np.random.randint(5, 95, size=len(repeated_loans)), 0)
light_late_mask = (repeated_defaults == 0) & (np.random.rand(len(repeated_loans)) > 0.92)
days_late_gen[light_late_mask] = np.random.randint(1, 15, size=np.sum(light_late_mask))

start_date = datetime.date(2023, 1, 1)
date_offsets = [start_date + datetime.timedelta(days=int(30 * i)) for i in p_idx]

fact_payments = pd.DataFrame({
    'payment_id': [f"PMT{str(x).zfill(10)}" for x in range(1, len(repeated_loans) + 1)],
    'loan_id': repeated_loans,
    'payment_date': date_offsets,
    'amount_paid': np.round(base_payment_amt, 2),
    'days_late': days_late_gen
})

drop_mask = (repeated_defaults == 1) & (p_idx > np.random.randint(1, 4, size=len(repeated_loans)))
fact_payments = fact_payments[~drop_mask]

# Force-drop duplicate payment records if any were generated in the math loops
if 'payment_id' in fact_payments.columns:
    fact_payments = fact_payments.drop_duplicates(subset=['payment_id'])

# Stream out payments using a slightly safer chunksize for massive sets
fact_payments.to_sql('fact_payment_history', engine, if_exists='append', index=False, chunksize=50000)
print(f"  ✔ fact_payment_history loaded with {len(fact_payments)} entries.")

# =========================================================
# 6. DIM CREDIT BUREAU EXTENSION
# =========================================================
print("⏳ Generating Credit Bureau Records...")

dim_bureau = pd.DataFrame({
    'customer_id': fact_loan['customer_id'],
    'credit_score': fact_loan['credit_score'],
    'credit_utilization': np.round(np.random.uniform(0.05, 0.95, size=len(fact_loan)), 2),
    'previous_defaults': np.where(fact_loan['credit_score'] < 580, np.random.randint(1, 4, size=len(fact_loan)), 0),
    'hard_inquiries': np.random.randint(0, 8, size=len(fact_loan))
})

dim_bureau.to_sql('dim_credit_bureau', engine, if_exists='append', index=False, chunksize=10000)
print("  ✔ dim_credit_bureau loaded.")

print("\n🎉 SUCCESS: Data Warehouse is fully packed with over 2 Million structured records!")