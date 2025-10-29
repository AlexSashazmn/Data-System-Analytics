[English version](TASK2_LOGIC.en.md)
# Задача 2: Модель данных

На этом этапе была создана единая модель данных, объединяющая разрозненные источники (Google Ads, Facebook Ads, MMP) в одну аналитическую таблицу. Это позволило подготовить данные для дальнейшей визуализации и анализа в Power BI.

---

## Процесс подготовки данных

**Создание базы данных:** С помощью MySQL была создана база данных с названием digital_marketing.

**Импорт данных:** Для импорта CSV-файлов (ads_facebook_ads_last.csv, ads_google_ads_last.csv, mmp_last.csv) в созданную базу данных, использовался DBeaver, соединенный с MySQL.

**Выполнение скрипта:** Для объединения и агрегации данных была использована среда DBeaver'а, в ней выполнялся SQL-скрипт.

---

## Логика объединения и нормализации

**Правило мэтчинга:** Данные из рекламных каналов (Google, Facebook) и данные из MMP (Adjust/AppsFlyer) были сведены с использованием LEFT JOIN. Ключами для объединения послужили campaign_id и дата (ad_date = install_date), что обеспечивает точное сопоставление дневных затрат и результатов по каждой кампании.

**Нормализация:** Поскольку мэтчинг производился по уникальному идентификатору campaign_id, сложная нормализация поля campaign_name не потребовалась. Этот подход является более надежным и предотвращает ошибки, связанные с возможными расхождениями в названиях.

**Агрегация:** Данные были сгруппированы по дате, источнику, ID и названию кампании для получения итоговых дневных показателей.

---

## SQL-скрипт для создания агрегированной таблицы данных

Следующий SQL-скрипт использовался для создания итоговой таблицы aggregated_paid_ads.

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

## Расчетные метрики (DAX в Power BI)

Для обеспечения гибкости анализа и корректного пересчета итоговых значений при использовании фильтров, все ключевые метрики были рассчитаны в Power BI с помощью мер (Measures) на языке DAX. Этот подход позволяет избежать ошибок усреднения, которые могут возникнуть при расчете метрик в SQL.

### CTR (Click-Through Rate):

```dax
CTR = 
DIVIDE(
   SUM('aggregated_paid_ads'[Clicks]),
    SUM('aggregated_paid_ads'[Impressions]),
    0
)
```

### CPI (Cost Per Install):

```dax
CPI = 
DIVIDE(
    SUM('aggregated_paid_ads'[Spend]),
    SUM('aggregated_paid_ads'[Installs]),
    BLANK()
)
```

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

```dax
ROAS_D7 = 
DIVIDE(
    SUM('aggregated_paid_ads'[D7 Revenue]),
    SUM('aggregated_paid_ads'[Spend]),
    BLANK()
)
```

### CPC (Cost Per Click):

```dax
CPC = 
DIVIDE(
    SUM('aggregated_paid_ads'[Spend]), 
    SUM('aggregated_paid_ads'[Clicks]), 
    BLANK()
)
```

### CPM (Cost Per Mille):

```dax
CPM = 
DIVIDE(
    SUM('aggregated_paid_ads'[Spend]), 
    SUM('aggregated_paid_ads'[Impressions]), 
    BLANK()
) * 1000
```
