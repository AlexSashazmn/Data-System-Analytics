[Русская версия](TASK3_DASHBOARD_OVERVIEW.md)
# Task 3: Dashboard in Power BI

## Project Overview

This project demonstrates the development of an analytical dashboard in **Power BI** to evaluate the performance of paid advertising campaigns on **Google Ads** and **Facebook Ads**.

The dataset used is **synthetic**, generated via a Python script and aggregated in SQL to simulate realistic campaign metrics and ensure the reproducibility of the analysis.

---

## Objectives

As per the task requirements, the dashboard includes:

- **KPI Cards or Matrices**: Spend, Installs, ROAS D1/D7, CTR, CPI
- **Time Series Chart**: Daily Spend and Installs (line chart)
- **Campaign Table**: Spend, Installs, CPI, ROAS D1, ROAS D7
- **Slicers**: Source (Google/Meta), date range
- **Deliverables**: `.pbix` file + README documentation

---

## Data Sources

- **Advertising Data**:
    - `ads_facebook_ads_last`
    - `ads_google_ads_last`
- **MMP Data**:
    - `mmp_last`

The data was joined on `campaign_id` and `date` using SQL, then imported into Power BI.

---

## Data Model

- Advertising data was combined using `UNION ALL`
- Joined with MMP data using a `LEFT JOIN` on `campaign_id` + `date`
- Calculated fields for CTR, CPI, CPC, CPM, ROAS D1, and ROAS D7 were added using **DAX** code in **Power BI**

<p align="left">
<img src="https://github.com/user-attachments/assets/a181be9e-a44d-49c3-8c03-c541dbe27529" width="33%" />
</p>

---

## Key Metrics (DAX)

```
CTR = DIVIDE(SUM('aggregated_paid_ads'[Clicks]), SUM('aggregated_paid_ads'[Impressions]), 0)

CPI = DIVIDE(SUM('aggregated_paid_ads'[Spend]), SUM('aggregated_paid_ads'[Installs]), BLANK())

ROAS_D1 = DIVIDE(SUM('aggregated_paid_ads'[D1 Revenue]), SUM('aggregated_paid_ads'[Spend]), BLANK())

ROAS_D7 = DIVIDE(SUM('aggregated_paid_ads'[D7 Revenue]), SUM('aggregated_paid_ads'[Spend]), BLANK())

CPC = DIVIDE(SUM('aggregated_paid_ads'[Spend]), SUM('aggregated_paid_ads'[Clicks]), BLANK())

CPM = DIVIDE(SUM('aggregated_paid_ads'[Spend]), SUM('aggregated_paid_ads'[Impressions]), BLANK()) * 1000

```

---

## Dashboard Pages

- **Overview**: Key KPIs and trends
- **Google Ads**: Detailed campaign performance with sparklines
- **Facebook Ads**: Detailed campaign performance with sparklines

<p align="center">
<img src="https://github.com/user-attachments/assets/62212e6b-0193-4501-8aca-17cae945af44" width="33%" />
<img src="https://github.com/user-attachments/assets/9426029b-96a1-40eb-94b9-f04ea73e53b5" width="33%" />
<img src="https://github.com/user-attachments/assets/2b0f0c33-d263-4db2-ab99-d23c16864293" width="33%" />
</p>

---

## How to Use

1. Clone this repository
2. Download the `paid_ads_analysis_dashboard.pbix` file
3. Open it in **Power BI Desktop**

---

### Disclaimer

All data is **synthetic** and does not reflect actual business results.

This project is intended solely to demonstrate skills in Python, SQL, DAX, and Power BI.
