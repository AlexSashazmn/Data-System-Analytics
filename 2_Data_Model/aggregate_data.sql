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
