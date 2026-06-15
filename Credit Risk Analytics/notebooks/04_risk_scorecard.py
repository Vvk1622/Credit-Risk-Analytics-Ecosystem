import pandas as pd

# ==================================================
# LOAD DATA
# ==================================================

df = pd.read_csv("../data/raw/loan_default.csv")

# ==================================================
# CHECK CREDIT SCORE RANGE
# ==================================================

print("Credit Score Range")
print("Min:", df['CreditScore'].min())
print("Max:", df['CreditScore'].max())

# ==================================================
# INCOME SCORE
# Low Income = High Risk
# High Income = Low Risk
# ==================================================

df['IncomeScore'] = pd.qcut(
    df['Income'],
    q=4,
    labels=[4, 3, 2, 1]
).astype(int)

# ==================================================
# CREDIT SCORE RISK BAND
# ==================================================

df['CreditBand'] = pd.cut(
    df['CreditScore'],
    bins=[-1, 500, 600, 700, 1000],
    labels=[4, 3, 2, 1]
)

# Convert category to integer
df['CreditBand'] = df['CreditBand'].astype(int)

# ==================================================
# EMPLOYMENT SCORE
# ==================================================

employment_map = {
    'Unemployed': 4,
    'Part-time': 3,
    'Self-employed': 2,
    'Full-time': 1
}

df['EmploymentScore'] = df['EmploymentType'].map(employment_map)

# ==================================================
# FINAL RISK SCORE
# ==================================================

df['RiskScore'] = (
    df['IncomeScore']
    + df['CreditBand']
    + df['EmploymentScore']
)

# ==================================================
# CREATE RISK CATEGORY
# ==================================================

df['RiskCategory'] = pd.cut(
    df['RiskScore'],
    bins=[0, 4, 7, 9, 12],
    labels=[
        'Low Risk',
        'Medium Risk',
        'High Risk',
        'Very High Risk'
    ]
)

# ==================================================
# SAMPLE OUTPUT
# ==================================================

print("\nSample Records")
print(
    df[
        [
            'Income',
            'CreditScore',
            'EmploymentType',
            'IncomeScore',
            'CreditBand',
            'EmploymentScore',
            'RiskScore',
            'RiskCategory'
        ]
    ].head(10)
)

# ==================================================
# RISK CATEGORY DISTRIBUTION
# ==================================================

print("\nRisk Category Distribution")
print(df['RiskCategory'].value_counts())

# ==================================================
# DEFAULT RATE BY RISK CATEGORY
# ==================================================

print("\nDefault Rate By Risk Category")

risk_default = pd.crosstab(
    df['RiskCategory'],
    df['Default'],
    normalize='index'
) * 100

print(risk_default.round(2))