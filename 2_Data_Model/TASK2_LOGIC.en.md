[Русская версия](TASK2_LOGIC.md)
# Task 2: Data Model

At this stage, a unified data model was created, combining disparate sources (Google Ads, Facebook Ads, MMP) into a single analytical table. This prepared the data for further visualization and analysis in Power BI.

---

## Data Preparation Process

**Database Creation:** A database named `digital_marketing` was created using MySQL.

**Data Import:** DBeaver, connected to MySQL, was used to import the CSV files (`ads_facebook_ads_last.csv`, `ads_google_ads_last.csv`, `mmp_last.csv`) into the created database.

**Script Execution:** An SQL script was executed in the DBeaver environment to join and aggregate the data.

---

## Join and Normalization Logic

**Matching Rule:** Data from the advertising channels (Google, Facebook) and data from the MMP (Adjust/AppsFlyer) were combined using a `LEFT JOIN`. The keys for the join were `campaign_id` and date (`ad_date = install_date`), ensuring an accurate match of daily costs and results for each campaign.

**Normalization:** Since the matching was performed using the unique `campaign_id`, complex normalization of the `campaign_name` field was not required. This approach is more reliable and prevents errors related to potential discrepancies in names.

**Aggregation:** The data was grouped by date, source, campaign ID, and campaign name to obtain final daily metrics.

---

## SQL Script for Creating the Aggregated Data Table

The following SQL script was used to create the final `aggregated_paid_ads` table.

```sql
USE digital_marketing;
CREATE TABLE aggregated_paid_ads
WITH
FacebookAds AS (
    SELECT
        date AS ad_date,
        source,
        campaign_id,
        campaign_name,
        impressions,
        clicks,
        spend
    FROM ads_facebook_ads_last
),
GoogleAds AS (
    SELECT
        date AS ad_date,
        source,
        campaign_id,
        campaign_name,
        impressions,
        clicks,
        spend
    FROM ads_google_ads_last
),
CombinedAds AS (
    SELECT * FROM FacebookAds
    UNION ALL
    SELECT * FROM GoogleAds
),
MMPData AS (
    SELECT
        date AS install_date,
        campaign_id,
        installs,
        d1_revenue,
        d7_revenue
    FROM mmp_last
)
SELECT
    ads.ad_date,
    ads.source,
    ads.campaign_id,
    ads.campaign_name,
    SUM(ads.impressions) AS total_impressions,
    SUM(ads.clicks) AS total_clicks,
    SUM(CAST(ads.spend AS DECIMAL(18,4))) AS total_spend,
    IFNULL(SUM(mmp.installs), 0) AS total_installs,
    IFNULL(SUM(mmp.d1_revenue), 0) AS total_d1_revenue,
    IFNULL(SUM(mmp.d7_revenue), 0) AS total_d7_revenue
FROM CombinedAds AS ads
LEFT JOIN MMPData AS mmp
  ON ads.campaign_id = mmp.campaign_id
  AND ads.ad_date = mmp.install_date
GROUP BY
    ads.ad_date,
    ads.source,
    ads.campaign_id,
    ads.campaign_name
ORDER BY
    ads.ad_date,
    ads.source,
    total_spend DESC

```

---

## Calculated Metrics (DAX in Power BI)

To ensure analytical flexibility and the correct recalculation of totals when using filters, all key metrics were calculated in Power BI using **Measures** in the DAX language. This approach avoids the averaging errors that can occur when calculating metrics in SQL.

### CTR (Click-Through Rate):

```
CTR =
DIVIDE(
   SUM('aggregated_paid_ads'[Clicks]),
    SUM('aggregated_paid_ads'[Impressions]),
    0
)

```

### CPI (Cost Per Install):

```
CPI =
DIVIDE(
    SUM('aggregated_paid_ads'[Spend]),
    SUM('aggregated_paid_ads'[Installs]),
    BLANK()
)```

### ROAS D1 (Return On Ad Spend, Day 1):

```dax
ROAS_D1 =
DIVIDE(
    SUM('aggregated_paid_ads'[D1 Revenue]),
    SUM('aggregated_paid_ads'[Spend]),
    BLANK()
)

```

### ROAS D7 (Return On Ad Spend, Day 7):

```
ROAS_D7 =
DIVIDE(
    SUM('aggregated_paid_ads'[D7 Revenue]),
    SUM('aggregated_paid_ads'[Spend]),
    BLANK()
)

```

### CPC (Cost Per Click):

```
CPC =
DIVIDE(
    SUM('aggregated_paid_ads'[Spend]),
    SUM('aggregated_paid_ads'[Clicks]),
    BLANK()
)

```

### CPM (Cost Per Mille):

```
CPM =
DIVIDE(
    SUM('aggregated_paid_ads'[Spend]),
    SUM('aggregated_paid_ads'[Impressions]),
    BLANK()
) * 1000

```
