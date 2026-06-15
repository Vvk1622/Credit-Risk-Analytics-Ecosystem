import pandas as pd
pd.set_option('display.ma
x_columns', None)

# Load Dataset
df = pd.read_csv("../data/raw/loan_default.csv")

# ==========================================================
# DATASET OVERVIEW
# ==========================================================

print("=" * 80)
print("DATASET SHAPE")
print("=" * 80)

print(df.shape)

# ==========================================================
# DEFAULT DISTRIBUTION
# ==========================================================

print("\n")
print("=" * 80)
print("DEFAULT DISTRIBUTION")
print("=" * 80)

print(df['Default'].value_counts())

# ==========================================================
# DEFAULT RATE
# ==========================================================

print("\n")
print("=" * 80)
print("DEFAULT RATE")
print("=" * 80)

default_rate = df['Default'].mean() * 100

print(f"Default Rate: {default_rate:.2f}%")

# ==========================================================
# CREDIT SCORE ANALYSIS
# ==========================================================

print("\n")
print("=" * 80)
print("CREDIT SCORE ANALYSIS")
print("=" * 80)

print(
    df.groupby('Default')['CreditScore'].mean()
)

# ==========================================================
# DTI ANALYSIS
# ==========================================================

print("\n")
print("=" * 80)
print("DTI ANALYSIS")
print("=" * 80)

print(
    df.groupby('Default')['DTIRatio'].mean()
)

# ==========================================================
# INCOME ANALYSIS
# ==========================================================

print("\n")
print("=" * 80)
print("INCOME ANALYSIS")
print("=" * 80)

print(
    df.groupby('Default')['Income'].mean()
)

# ==========================================================
# LOAN AMOUNT ANALYSIS
# ==========================================================

print("\n")
print("=" * 80)
print("LOAN AMOUNT ANALYSIS")
print("=" * 80)

print(
    df.groupby('Default')['LoanAmount'].mean()
)

# ==========================================================
# NUMERIC RISK DRIVERS
# ==========================================================

print("\n")
print("=" * 80)
print("NUMERIC RISK DRIVERS")
print("=" * 80)

result = df.groupby('Default')[
    [
        'Income',
        'LoanAmount',
        'CreditScore',
        'MonthsEmployed',
        'NumCreditLines',
        'InterestRate',
        'LoanTerm',
        'DTIRatio'
    ]
].mean()

print(result.T)

# ==========================================================
# EDUCATION ANALYSIS
# ==========================================================

print("\n")
print("=" * 80)
print("EDUCATION ANALYSIS")
print("=" * 80)

education = pd.crosstab(
    df['Education'],
    df['Default'],
    normalize='index'
) * 100

print(education.round(2))

# ==========================================================
# EMPLOYMENT ANALYSIS
# ==========================================================

print("\n")
print("=" * 80)
print("EMPLOYMENT ANALYSIS")
print("=" * 80)

employment = pd.crosstab(
    df['EmploymentType'],
    df['Default'],
    normalize='index'
) * 100

print(employment.round(2))

# ==========================================================
# EDUCATION + EMPLOYMENT ANALYSIS
# ==========================================================

print("\n")
print("=" * 80)
print("EDUCATION + EMPLOYMENT ANALYSIS")
print("=" * 80)

edu_emp = pd.crosstab(
    [df['EmploymentType'], df['Education']],
    df['Default'],
    normalize='index'
) * 100

print(edu_emp.round(2))

# ==========================================================
# CREDIT SCORE BANDS
# ==========================================================

print("\n")
print("=" * 80)
print("CREDIT SCORE BAND ANALYSIS")
print("=" * 80)

df['CreditScoreBand'] = pd.cut(
    df['CreditScore'],
    bins=[300, 500, 600, 700, 850],
    labels=[
        'Poor',
        'Fair',
        'Good',
        'Excellent'
    ]
)

credit_band = pd.crosstab(
    df['CreditScoreBand'],
    df['Default'],
    normalize='index'
) * 100

print(credit_band.round(2))

# ==========================================================
# INCOME BANDS
# ==========================================================

print("\n")
print("=" * 80)
print("INCOME BAND ANALYSIS")
print("=" * 80)

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

income_band = pd.crosstab(
    df['IncomeBand'],
    df['Default'],
    normalize='index'
) * 100

print(income_band.round(2))

# ==========================================================
# INCOME + EMPLOYMENT RISK MATRIX
# ==========================================================

print("\n")
print("=" * 80)
print("INCOME + EMPLOYMENT RISK MATRIX")
print("=" * 80)

risk_matrix = pd.crosstab(
    [df['IncomeBand'], df['EmploymentType']],
    df['Default'],
    normalize='index'
) * 100

print(risk_matrix.round(2))