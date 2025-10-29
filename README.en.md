[Русская версия](README.md)

# Advertising Campaign Performance Analysis (Google & Facebook Ads)

## Brief Description
This repository contains a comprehensive solution to a test task on analyzing paid traffic data. The project covers the full data lifecycle: from generating synthetic data to preparing analytical conclusions and recommendations.

---

## Project Structure

- **/1_Data_Emulation/**: A Python script for generating the source CSV files.
- **/2_Data_Model/**: An SQL script for data consolidation and a description of the DAX metric logic.
- **/3_Dashboard/**: The Power BI dashboard file (.pbix) with visualizations and screenshots.
- **/4_Conclusions/**: Brief conclusions and recommendations for campaign optimization.

---

## Technology Stack

- **Data Generation:** Python
- **Storage and Processing:** MySQL; DBeaver
- **Modeling and Visualization:** Power BI; DAX
- **Version Control:** Git; GitHub

---

## Task 1: Data Collection and Emulation

**Description**
At this stage, data for a 14-day period was synthesized to simulate the performance metrics of advertising campaigns from Google Ads, Facebook Ads, and a mobile measurement partner (MMP).

**Tool**
- Python script: `synthet_ads_mmp.py`

**Result**
- Three CSV files: `ads_facebook_ads_last_14_days.csv`; `ads_google_ads_last_14_days.csv`; `mmp_last_14_days.csv` — ready to be loaded into a database.

**Execution Instructions**
Full instructions for running the script can be found in `/1_Data_Emulation/TASK1_INSTRUCTIONS.md`.

---

## Task 2: Data Model

**Description**
The CSV files were uploaded to a database created in MySQL via DBeaver and combined into a single analytical data mart using SQL. Key metrics were calculated in Power BI using DAX to ensure correct analysis.

**Join Logic**
- Data from advertising platforms and the MMP were matched by `campaign_id` and `date` using a `LEFT JOIN`.

**Metric Calculation**
- All metrics (CTR, CPI, ROAS, etc.) were implemented as **Measures** in Power BI for accurate calculation of final values.

**Artifacts**
- The full SQL script and a description of the DAX formulas are available in `/2_Data_Model/TASK2_LOGIC.md`.

---

## Task 3: Dashboard in Power BI

**Description**
An interactive dashboard was created based on the prepared data model for the visual analysis of campaign performance.

**Key Dashboard Elements**
- **Overall KPIs:** Cards or matrices with summary indicators (Spend, Installs, ROAS D7, CTR, CPI).
- **Dynamics:** Charts showing the daily changes in costs and installs.
- **Details:** A table with complete statistics for each campaign.
- **Filters:** The ability to analyze data by source (Google / Facebook) and by date.

**Files**
- The `.pbix` file and dashboard screenshots are located in `/3_Dashboard/TASK3_DASHBOARD_OVERVIEW.md`.

<p align="center">
  <img src="https://github.com/user-attachments/assets/62212e6b-0193-4501-8aca-17cae945af44" width="30%" />
  <img src="https://github.com/user-attachments/assets/9426029b-96a1-40eb-94b9-f04ea73e53b5" width="30%" />
  <img src="https://github.com/user-attachments/assets/2b0f0c33-d263-4db2-ab99-d23c16864293" width="30%" />
</p>

---

## Task 4: Key Conclusions and Recommendations

**Analysis Period**
- October 7 — 20, 2025

### Main Results

**Campaigns to Scale**

- **Google Ads: UAC – Value | Android | APAC | Video** — Highest ROAS D7 at **1166.04%**, low CPI of **$1.89**, and spend of **$3,087**; scale the budget.
- **Facebook Ads: UA – Retargeting – Value | iOS | LATAM | UGC** — ROAS D7 of **1121.52%**, CPI of **$2.25**, and spend of **$1,157**; a priority for increasing reach.
- **Google Ads: UAC – Value | Android | EU | Playables** — ROAS D7 of **1018.53%**, **6,167** Installs, and spend of **$13,970**; scalable, maintains profitability with increased investment.

**Campaigns to Pause / Relaunch**

- **Google Ads: Search – Brand – Exact | iOS | US | UGC** — Low ROAS D7 of **307.30%**, the highest CPI at **$4.67**; stop and analyze creatives and targeting.
- **Facebook Ads: UA – Prospecting – Broad | IOS | US | USG** — High spend of **$17,922**, ROAS D7 of **443.07%**, and CPI of **$3.76**; pause and rework the audience/creatives.
- **Facebook Ads: UA – Prospecting – Broad | Android | LATAM | Static** — Spend of **$12,033** and ROAS D7 of **431.82%**; pause and fully optimize before resuming.

### Detailed Analysis
The full text analysis is available in the file `/4_Conclusions/TASK4_CONCLUSIONS.md`.
