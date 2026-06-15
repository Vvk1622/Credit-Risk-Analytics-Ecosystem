# Credit Risk & Capital Allocation Analytics Ecosystem
**System Architecture:** Power BI Enterprise Environment  

## Executive Summary
This project delivers a fully interactive, relational, 5-page Power BI dashboard designed to transform raw transaction and demographic data into institutional-grade credit intelligence. By moving away from siloed data structures, this solution builds a robust star-schema data model that connects credit bureau risk metrics, customer demographics, employment tier profiles, and loan intentions directly to a core transaction ledger.

## Python Exploratory Data Analysis (EDA)
Before building the relational model in Power BI, a comprehensive EDA was performed using Python (Pandas, NumPy, Matplotlib/Seaborn) to understand data distributions and clean anomalies:
* **Missing Value & Structure Analysis:** Inspected null distributions across primary keys and realized `branch_id` limitations early in the schema check.
* **Risk Core Correlations:** Calculated statistical correlations between borrower credit scores, hard inquiries, and ultimate `default_flag` rates to validate chart choices.
* **Leverage Insights:** Grouped and aggregated `dti_ratio` distributions across employment tiers to anticipate underlying data behavior.

## The Core Data Model Architecture
The entire analytics ecosystem relies on an optimized relational database schema to ensure flawless cross-filtering:
* **public fact_loan_performance (Central Fact Ledger):** Contains primary metrics: `loan_amount`, `interest_rate`, `dti_ratio`, `risk_score`, and `default_flag`.
* **public dim_customer:** Linked via `customer_id` with Cross Filter Direction set to **Both**.
* **public dim_credit_bureau:** Linked via `customer_id` with Cross Filter Direction set to **Both**.
* **public dim_loan_purpose & public dim_employment:** Tied directly to the central ledger via `purpose_id` and `employment_id` respectively.

## The 5-Page Dashboard Layout
* **Page 1: Executive Overview Dashboard** — High-level portfolio overview tracking overall portfolio exposure, total volumes, and baseline asset health.
* **Page 2: Credit Risk Dashboard** — Slices and monitors portfolio asset health by tracking credit score distributions, risk exposure tiers, and default trends.
* **Page 3: Branch Performance & Regional Risk** — Monitors geographical and macro risk vectors by tracking sector capital allocations and default concentrations across operational areas.
* **Page 4: Borrower Profile Analysis** — Deep dive into customer demographics, tracking how family profiling, marital status, and credit bureau inquiries explicitly impact default rates.
* **Page 5: Loan Purpose & Capital Deployment** — Tracks capital distribution across different workforce tiers, and analyzes which loan intents create the highest Debt-to-Income (DTI) leverage strains.
