-- Transfomrs hte customers table in bronze layer and inserts it into silver layer

with raw as (
    select * 
    from {{ source('bronze', 'customers') }}
    where cst_id is not null
),

cleaned as (
    select
        cst_id,
        cst_key,
        trim(cst_firstname) as cst_firstname,
        trim(cst_lastname) as cst_lastname,
        case 
            when upper(trim(cst_marital_status)) = 'M' then 'Married'
            when upper(trim(cst_marital_status)) = 'S' then 'Single'
            else 'Unknown'
        end as cst_marital_status,
        {{ trim_clean_gender('cst_gndr')}} as cst_gndr,
        cast(cst_create_date as date) as cst_create_date
    from raw
),

ranked as (
    select
        *,
        row_number() over (partition by cst_id order by cst_create_date desc) as rn
    from cleaned
)

select
    cst_id,
    cst_key,
    cst_firstname,
    cst_lastname,
    cst_marital_status,
    cst_gndr,
    cst_create_date
from ranked
where rn = 1
