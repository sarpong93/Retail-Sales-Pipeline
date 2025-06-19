with invoices as (
    select *
    from {{ source('retail_raw', 'invoices') }}
),

cleaned as (
    select
        invoice_id,
        customer_id,
        item_id,
        try_cast(invoice_date as date) as invoice_date,
        try_cast(due_date as date) as due_date,
        try_cast(quantity as int) as quantity,
        try_cast(rate as double) as rate,
        try_cast(amount as double) as amount,
        lower(trim(status)) as status
    from invoices
    where lower(trim(invoice_id)) != 'invoice_id'
),

joined as (
    select
        c.customer_name,
        c.email,
        i.item_name,
        i.category,
        f.*
    from cleaned f
    left join {{ ref('dim_customers') }} c using (customer_id)
    left join {{ ref('dim_items') }} i using (item_id)
)

select * from joined