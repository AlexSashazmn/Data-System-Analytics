[English version](TASK3_DASHBOARD_OVERVIEW.en.md)

# Задача 3: Дашборд в Power BI

## Обзор проекта

Данный проект демонстрирует разработку аналитического дашборда в **Power BI** для оценки эффективности платных рекламных кампаний в **Google Ads** и **Facebook Ads**.

Используемый датасет является **синтетическим**, сгенерированным с помощью Python‑скрипта и агрегированным в SQL, чтобы имитировать реалистичные показатели кампаний и обеспечить воспроизводимость анализа.

---

## Цели

Согласно требованиям задачи, дашборд включает:
- **KPI‑карточки или матрицы**: Spend, Installs, ROAS D1/D7, CTR, CPI  
- **График временного ряда**: ежедневные Spend и Installs (линейный график)  
- **Таблица кампаний**: Spend, Installs, CPI, ROAS D1, ROAS D7  
- **Слайсеры**: источник (Google/Meta), диапазон дат  
- **Результаты**: файл `.pbix` + документация README  

---

## Источники данных

- **Данные по рекламе**:
  - `ads_facebook_ads_last`
  - `ads_google_ads_last`
- **Данные MMP**:
  - `mmp_last`

Данные были объединены по `campaign_id` и `date` с помощью SQL, затем импортированы в Power BI.

---

## Модель данных

- Рекламные данные объединены через `UNION ALL`  
- Соединены с данными MMP с помощью `LEFT JOIN` по `campaign_id` + `date`  
- Добавлены вычисляемые поля для CTR, CPI, CPC, CPM, ROAS D1, ROAS D7 с помощью **DAX**-кода в **Power BI**
  
<p align="left">
  <img src="https://github.com/user-attachments/assets/a181be9e-a44d-49c3-8c03-c541dbe27529" width="33%" />
</p>

---

## Ключевые метрики (DAX)

```dax
CTR = DIVIDE(SUM('aggregated_paid_ads'[Clicks]), SUM('aggregated_paid_ads'[Impressions]), 0)

CPI = DIVIDE(SUM('aggregated_paid_ads'[Spend]), SUM('aggregated_paid_ads'[Installs]), BLANK())

ROAS_D1 = DIVIDE(SUM('aggregated_paid_ads'[D1 Revenue]), SUM('aggregated_paid_ads'[Spend]), BLANK())

ROAS_D7 = DIVIDE(SUM('aggregated_paid_ads'[D7 Revenue]), SUM('aggregated_paid_ads'[Spend]), BLANK())

CPC = DIVIDE(SUM('aggregated_paid_ads'[Spend]), SUM('aggregated_paid_ads'[Clicks]), BLANK())

CPM = DIVIDE(SUM('aggregated_paid_ads'[Spend]), SUM('aggregated_paid_ads'[Impressions]), BLANK()) * 1000
```

---

## Страницы дашборда

- **Обзор**: ключевые KPI и тренды  
- **Google Ads**: детальная эффективность кампаний со спарклайнами  
- **Facebook Ads**: детальная эффективность кампаний со спарклайнами  

<p align="center">
  <img src="https://github.com/user-attachments/assets/62212e6b-0193-4501-8aca-17cae945af44" width="33%" />
  <img src="https://github.com/user-attachments/assets/9426029b-96a1-40eb-94b9-f04ea73e53b5" width="33%" />
  <img src="https://github.com/user-attachments/assets/2b0f0c33-d263-4db2-ab99-d23c16864293" width="33%" />
</p>

---

## Как использовать

1. Клонируйте данный репозиторий  
2. Скачайте файл `paid_ads_analysis_dashboard.pbix`  
3. Откройте его в **Power BI Desktop**  

---

### Дисклеймер

Все данные являются **синтетическими** и не отражают реальные бизнес‑результаты.  

Проект предназначен исключительно для демонстрации навыков работы с Python, SQL, DAX и Power BI.  
