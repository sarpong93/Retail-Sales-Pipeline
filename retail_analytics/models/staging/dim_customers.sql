with raw as (
    select * 
    from {{ source('retail_raw', 'customers') }}
),

cleaned as (
    select
        customer_id,
        trim(customer_name) as customer_name,
        lower(trim(email)) as email,
        try_cast(created_date as date) as signup_date
    from raw
)

select * from cleaned
-- This model cleans and transforms the customer data from the raw source.
-- It ensures that customer names are properly capitalized, emails are in lowercase,
-- signup dates are cast to date type, and statuses are standardized to 'active', 'inactive', or 'unknown'.
-- The cleaned data can be used for further analysis or reporting in the retail analytics pipeline.
-- This model is part of the retail analytics project and is used to prepare customer data for analysis.