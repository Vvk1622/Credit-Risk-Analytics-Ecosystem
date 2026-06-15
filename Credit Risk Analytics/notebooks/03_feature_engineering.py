import pandas as pd

df = pd.read_csv("../data/raw/loan_default.csv")

# ==================================================
# CREDIT SCORE BAND
# ==================================================

df['CreditScoreBand'] = pd.cut(
    df['CreditScore'],
    bins=[300, 500, 600, 700, 850],
    labels=['Poor', 'Fair', 'Good', 'Excellent']
)

# ==================================================
# INCOME BAND
# ==================================================

df['IncomeBand'] = pd.qcut(
    df['Income'],
    q=4,
    labels=[
        'Low Income',
        'Lower-Mid',
        'Upper-Mid',
        'High Income'
    ]
)

# ==================================================
# EMPLOYMENT TENURE BAND
# ==================================================

df['EmploymentBand'] = pd.cut(
    df['MonthsEmployed'],
    bins=[-1,24,60,120,500],
    labels=['New','Mid','Experienced','Veteran']
)

print(df.head())

print("\nNew Columns Created:")
print([
    'CreditScoreBand',
    'IncomeBand',
    'EmploymentBand'
])