# 📊 Institutional Credit Risk & Capital Allocation Analytics Ecosystem

**Enterprise BI Architecture & Risk Modeling Framework** **Technology Stack:** Python (Pandas, NumPy, Seaborn) | Power BI Desktop & Service | PostgreSQL Backend  
**Author:** Vvk1622  

---

## 🎯 Executive Summary
This ecosystem delivers a production-ready, relational, 5-page Power BI business intelligence suite designed to convert raw multi-table transaction ledgers into credit intelligence. By replacing siloed, flat-file reporting methodologies, this solution establishes an optimized **Star-Schema Data Model** connecting credit bureau risk exposures, deep customer demographics, layered employment metrics, and borrowing intents directly to a centralized core transaction ledger. 

The architecture handles historical data validation, anomaly mitigation via programmatic Python Exploratory Data Analysis (EDA), structured entity-relationship configuration, and a strict, high-contrast **Sky Blue & Charcoal Corporate Design System** optimized for fast decision-making by risk committees.

---

## 🐍 Phase 1: Programmatic Python Exploratory Data Analysis (EDA)
Before initializing visual rendering pipelines, raw tables were extracted and processed via Python to map schema health, evaluate multi-collinearity, and profile critical risk trends.

### 1. Structure Verification & Anomaly Detection
``python
import pandas as pd
import numpy as np

# Load core datasets
fact_loans = pd.read_csv("public_fact_loan_performance.csv")
dim_customer = pd.read_csv("public_dim_customer.csv")

# Evaluating missingness profiling
print("--- Missing Value Analysis ---")
print(fact_loans.isnull().sum())

# Structural Integrity Check for high-cardinality keys
unique_customers_fact = fact_loans['customer_id'].nunique()
unique_customers_dim = dim_customer['customer_id'].nunique()
print(f"Fact Table Unique Customers: {unique_customers_fact}")
print(f"Dim Table Unique Customers: {unique_customers_dim}")

Critical Discovery: Structural analysis flagged a data gap where public dim_branch lacked an active map key inside the primary fact tables. The strategy shifted to utilize database views (public view_demographic_risk_profile) as highly performant aggregated processing layers to bridge regional metrics without fracturing the Star Schema.

import seaborn as sns
import matplotlib.pyplot as plt

# Merging bureau profiles with financial performance ledger
bureau_df = pd.read_csv("public_dim_credit_bureau.csv")
merged_risk = pd.merge(fact_loans, bureau_df, on='customer_id')

# Generate Correlation Matrix for High-Risk Variables
correlation_matrix = merged_risk[['credit_score', 'hard_inquiries', 'dti_ratio', 'default_flag']].corr()

plt.figure(figsize=(8, 6))
sns.heatmap(correlation_matrix, annot=True, cmap='Blues', fmt=".2f")
plt.title("Credit Risk Factor Correlations")
plt.savefig("screenshots/risk_correlation.png")

Key Analytical Insight: Python analytics proved a distinct mathematical correlation between elevated hard_inquiries and escalating default_flag occurrences. This correlation directly informed the engineering of the Page 4: Borrower Profile line trajectory chart.

Phase 2: Relational Data Model Architecture & Schematics
The stability of the sub-second filter processing speeds relies entirely on a clean, optimized relationship architecture inside Power BI.

1. Entity Relationship (ERD) Blueprint
                  [public dim_loan_purpose]
                             │ 
                             ▼ (1:*) via purpose_id
                             
[public dim_customer] ◄──► [public fact_loan_performance] ◄──► [public dim_employment]
         ▲     (1:*) via customer_id     ▲     (1:*) via employment_id
         │                               │
         └───────────► [public dim_credit_bureau] ◄┘
                       (1:1) via customer_id

2. Standard Configuration Specification MatrixTo eliminate visual component blanking errors, the following logical bounds were hardcoded:Origin TableTarget TableLinking KeyCardinality TypeCross-Filter Directionpublic dim_customerpublic fact_loan_performancecustomer_idOne-to-Many ($1:*$)Bothpublic dim_credit_bureaupublic fact_loan_performancecustomer_idMany-to-One ($*:1$)Bothpublic dim_loan_purposepublic fact_loan_performancepurpose_idMany-to-One ($*:1$)Single (Unidirectional)public dim_employmentpublic fact_loan_performanceemployment_idMany-to-One ($*:1$

Phase 3: Enterprise Design System Standards
The system adheres to rigid corporate design standards to maximize legibility and visual scanning efficiency:

The Palette: Dominant Charcoal Slate (#1E2229) for structure, crisp Off-White (#F4F6F9) for components backgrounds, and sharp Sky Blue (#00A2E8) for interactive fields.

Application-Style Slicers: Standard checkboxes were replaced by setting Visual Settings -> Slicer Style -> Tile.

Default Background: Light translucent grayish blue.

Active Selection: Focused Sky Blue background with white text and micro-rounded corners (5px padding).

KPI Card Banner Protocol: Default auto-generated bottom category labels were toggled OFF. Structured labels were explicitly turned ON in General Settings -> Title, formatted as bold, centered, medium-sized headers sitting directly over the metrics.


Phase 4: Production Dashboard Layer Specifications
📊 Page 1: Executive Overview Dashboard
Intent: High-level strategic visualization tracking portfolio exposure totals and immediate asset health visibility.

KPI Matrix: Sum of total_portfolio_exposure | Sum of total_loans_issued.

Visual Components: Vertical Clustered Column Chart mapping macro risk tiers versus volumetric allocations; Trend lines mapping rolling defaults over time.

🛡️ Page 2: Credit Risk Dashboard
Intent: Granular partitioning of portfolio asset health based on credit bureau score clustering.

Interactive Control: Modern Sky Blue Risk Category Slicer tiles.

Visual Components: Horizontal distribution matrix displaying avg_customer_income vs. avg_credit_score; Column chart tracking exposure allocations against credit categories.

🏢 Page 3: Branch Performance & Regional Risk
Intent: Isolation of geographical, branch network, and macro workforce-sector exposures.

Aggregated Layer Source: public view_demographic_risk_profile

Visual Components:

Chart A (Sector Capital Allocation): Clustered Column Chart plotting employment_type against total_allocated_capital, with risk_category in the Legend.

Chart B (Regional Vulnerabilities): Clustered Bar Chart exposing segment_default_rate_pct across regional workforces.

👥 Page 4: Borrower Profile Analysis
Intent: Micro-demographic deep-dive mapping personal lifestyle factors directly to portfolio risk.

Interactive Control: Dual Slicers for Marital Status and Home Ownership Status (Sky Blue Tiles).

Visual Components:

Chart A: Clustered Column Chart calculating credit_score variance across marital_status split by family dependency flags.

Chart B: Line Chart visualizing explicit Average of default_flag mapped along a continuous hard_inquiries X-axis to verify inquiry stress.

💼 Page 5: Loan Purpose & Capital Deployment
Intent: Tracking intended loan use cases against real-world household debt strain.

Interactive Control: Loan Intent Slicer (loan_purpose field).

Visual Components:

Chart A: Clustered Column Chart sizing loan_amount deployments against corporate employment_type sectors and salary experience bands.

Chart B: Horizontal Clustered Bar Chart evaluating the Average of dti_ratio across different borrowing use cases to flag highly leveraged categories.
                       
