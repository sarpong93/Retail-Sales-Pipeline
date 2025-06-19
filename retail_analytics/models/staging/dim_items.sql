with raw as (
    select * 
    from {{ source('retail_raw', 'items') }}
),

cleaned as (
    select
        item_id,
        trim(item_name) as item_name,
        lower(trim(category)) as category,
        try_cast(unit_price as double) as price
    from raw
)

select * from cleaned
