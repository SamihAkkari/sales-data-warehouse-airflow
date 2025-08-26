with cleaned_product as (
    select 
        prd_id,
        replace(substring(prd_key, 1, 5), '-', '_') as cat_id,
        substring(prd_key, 7, length(prd_key)) as prd_key,
        trim(prd_nm) as prd_nm,
        prd_cost,
        prd_line,
        cast(prd_start_dt as date) as prd_start_dt,
        lead (cast(prd_start_dt as date)) over (partition by prd_key order by cast(prd_start_dt as date) ASC) - 1 as prd_end_dt
    from {{ source('bronze', 'products') }}
) 

select * from cleaned_product