with base as (
  select 
    customer_id,
    amount,
    try_cast(invoice_date AS date) as invoice_date
  from {{ source('retail_raw', 'invoices') }}
),

summary as (
  select 
    customer_id,
    cast(date_trunc('month', invoice_date) as date) as month,
    count(*) as num_invoices,
    sum(amount) as total_spent
  from base
  group by 
    customer_id, 
    date_trunc('month', invoice_date)
)

select * from summary