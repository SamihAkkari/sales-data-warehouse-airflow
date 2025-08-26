select 
    {{generate_surrogate_key('pr.prd_id')}} as product_key,
    pr.prd_id as product_id,
    pr.cat_id as category_id,
    pr.prd_key as product_number,
    pr.prd_nm as product_name,
    pr.prd_cost as product_cost,
    pr.prd_line as product_line,
    pr.prd_start_dt as start_date,
    p.cat as category,
    p.subcat as subcategory,
    p.maintenance as maintenance
from {{ref('products')}} pr
left join {{ref('px')}} p
on pr.cat_id = p.id
where pr.prd_end_dt is null