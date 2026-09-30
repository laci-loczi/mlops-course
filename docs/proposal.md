# Project Proposal: Telco Customer Churn Prediction

## 1. Dataset

* **Name and brief description:** Telco Customer Churn dataset containing customer demographic data, account information, and service usage to predict whether a customer will leave the company within the last month.
* **Source URL and license:** Originally sourced from IBM sample datasets (commonly hosted on Kaggle under open licenses / MIT or equivalent).
* **Rough size:** 7,043 rows and ~20 features.
* **Mini data dictionary:**
  * `customerID`: Unique customer ID (String, format: XXXX-XXXXX, trustworthy).
  * `gender`: Customer gender (Categorical: Male, Female, trustworthy).
  * `SeniorCitizen`: Whether the customer is a senior citizen (Binary: 0, 1, trustworthy).
  * `tenure`: Number of months the customer has stayed with the company (Integer, range: 0–72 months, trustworthy).
  * `MonthlyCharges`: The amount charged to the customer monthly (Float, range: 18.0–120.0 USD, trustworthy).
  * `TotalCharges`: The total amount charged to the customer (Float, range: 0.0–8,684.0 USD, **untrustworthy**: contains blank values for ~11 new customers with 0 tenure, which must be handled).
  * `Churn`: Whether the customer churned or not (Binary: Yes/No, target column, trustworthy).

## 2. Prediction task

* **Target column:** `Churn` (mapped to 1 for "Yes" and 0 for "No").
* **Task type:** Binary classification.
* **Why it is interesting/useful:** Customer churn prediction is a core business problem in the telecommunications industry. Accurately identifying high-risk customers allows companies to proactively target them with retention offers, reducing customer acquisition costs and revenue loss.

## 3. Suitability check

* **Memory and training speed:** The dataset contains roughly 7,000 rows, easily fitting into memory on a 16 GB laptop. Training a baseline scikit-learn model takes well under 5 seconds.
* **Known limitation/quirk:** There is a class imbalance (~27% churn rate) and genuine missing/blank values in the `TotalCharges` column that need data cleaning before modeling.

## 4. Baseline idea

* **First scikit-learn model:** `LogisticRegression` (with `StandardScaler` for numeric features and `OneHotEncoder` for categorical features via a `Pipeline`).
* **Primary metric:** **ROC-AUC** (or **F1-score**), because the dataset is imbalanced and we care equally about precision and recall in identifying churners.