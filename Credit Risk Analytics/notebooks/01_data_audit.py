import pandas as pd

df = pd.read_csv("../data/raw/loan_default.csv")

print(df.shape)

print(df.head())
print(df.columns.tolist())
print(df.info())
print(df['Default'].value_counts())
print(
    df.groupby('Default')['CreditScore'].mean()
)
print(
    df.groupby('Default')['DTIRatio'].mean()
)


print(
    df.groupby('Default')['Income'].mean()
)
print(
    df.groupby('Default')['LoanAmount'].mean()
)
import pandas as pd

df = pd.read_csv("../data/raw/loan_default.csv")
#
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
import pandas as pd

df = pd.read_csv("../data/raw/loan_default.csv")

result = pd.crosstab(
    df['EmploymentType'],
    df['Default'],
    normalize='index'
) * 100

print(result)
import pandas as pd

df = pd.read_csv("../data/raw/loan_default.csv")

result = pd.crosstab(
    [df['EmploymentType'], df['Education']],
    df['Default'],
    normalize='index'
) * 100

print(result.round(2))
import pandas as pd

df = pd.read_csv("../data/raw/loan_default.csv")

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

result = pd.crosstab(
    df['CreditScoreBand'],
    df['Default'],
    normalize='index'
) * 100

print(result.round(2))
import pandas as pd

df = pd.read_csv("../data/raw/loan_default.csv")

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

result = pd.crosstab(
    df['IncomeBand'],
    df['Default'],
    normalize='index'
) * 100

print(result.round(2))
import pandas as pd

df = pd.read_csv("../data/raw/loan_default.csv")

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

result = pd.crosstab(
    [df['IncomeBand'], df['EmploymentType']],
    df['Default'],
    normalize='index'
) * 100

print(result.round(2))