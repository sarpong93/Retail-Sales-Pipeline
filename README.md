# 🛍️ Retail Sales Analytics Pipeline

A complete end-to-end data engineering project for ingesting, modeling, and analyzing retail sales data using cloud-native tools.

## 📌 Project Overview

This pipeline simulates a modern retail data platform, covering:
- Ingestion of raw `.csv` files into a cloud data lake (Amazon S3)
- Schema registration via AWS Glue
- Querying and partitioning via Amazon Athena
- Data modeling and transformation using `dbt`
- Outputting analytics-friendly models such as invoice summaries, customer profiles, and product-level insights

## 🧰 Tech Stack

| Layer       | Tool/Service        |
|-------------|---------------------|
| Ingestion   | Python + Boto3      |
| Storage     | Amazon S3           |
| Catalog     | AWS Glue            |
| Query Engine| Amazon Athena       |
| Modeling    | dbt (Athena adapter)|

## 🧱 Data Pipeline Architecture

                   +------------------+
                   |  CSV Input Files |
                   +--------+---------+
                            |
                            v
          +------------------------------+
          | Python ingestion script      |
          | - Validates schema           |
          | - Uploads to partitioned S3  |
          +------------------------------+
                            |
                            v
      +--------------------------------------+
      | Amazon S3 (raw zone, daily partition)|
      +--------------------------------------+
                            |
                            v
           +----------------------------+
           | AWS Glue Data Catalog      |
           +----------------------------+
                            |
                            v
                 +-----------------+
                 | Amazon Athena   |
                 +-----------------+
                            |
                            v
               +----------------------+
               | dbt Transformations  |
               +----------------------+
                            |
                            v
             +----------------------------+
             | Final models (in Athena)   |
             +----------------------------+

## 📂 Project Structure

Retail-Sales-Pipeline/
├── README.md
├── ingestion/
│   └── ingest_sales_data.py
├── test_data/
│   ├── invoices.csv
│   ├── customers.csv
│   └── items.csv
├── models/
│   ├── staging/
│   │   ├── dim_customers.sql
│   │   ├── dim_items.sql
        ├── invoice_summary.sql
│   │   └── stg_retail_sources.yml
│   └── core/
│       ├── fct_invoices.sql
└── dbt_project.yml

## 🧪 Key dbt Models

| Model Name            | Purpose                                             |
|-----------------------|-----------------------------------------------------|
| `dim_customers`       | Cleaned, deduplicated customer info                |
| `dim_items`           | Cleaned, standardized product catalog              |
| `fct_invoices`        | Line-item invoice fact table with dimension joins  |
| `invoice_summary`     | Monthly rollup of invoices per customer            |

## ⚙️ How to Run

### ✅ Prerequisites
- Python 3.10+
- AWS CLI configured (`aws configure`)
- AWS services enabled: S3, Glue, Athena
- `dbt` installed with [Athena adapter](https://docs.getdbt.com/docs/available-adapters/athena)

### 🚀 1. Ingest CSVs to S3

```bash
python ingestion/ingest_sales_data.py
```

### 🧠 2. Create and Repair Glue Tables

```sql
MSCK REPAIR TABLE retail_raw.invoices;
MSCK REPAIR TABLE retail_raw.customers;
MSCK REPAIR TABLE retail_raw.items;
```

OR:

```sql
ALTER TABLE retail_raw.table_name
ADD IF NOT EXISTS 
PARTITION (year=2025, month=06, day=17)
LOCATION 's3://qle-retail-pipeline/raw/customers/year=2025/month=06/day=17/';
```

### 🏗 3. Run dbt Models

```bash
dbt debug
dbt run
```

## 🔍 Sample Queries

```sql

-- Monthly revenue trend
SELECT month, SUM(total_spent) as revenue
FROM retail_models.invoice_summary
GROUP BY month
ORDER BY month;
```

## 📈 Future Improvements

- Add dbt tests and documentation
- Integrate Airflow for scheduled ingestion
- Add real-time ingestion from an API (e.g., Stripe, QuickBooks)
- Visualize with Looker Studio, Tableau, or QuickSight

## 🧑‍💻 Author

**Papa Yaw Sarpong**  
_Data Engineer | Portfolio Project_

## 📎 License

This project is open-source and intended for educational and demonstration purposes.
