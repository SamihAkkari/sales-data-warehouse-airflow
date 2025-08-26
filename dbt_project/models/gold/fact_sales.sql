
select
    s.sls_ord_num as order_number,
    c.customer_key as customer_key,
    p.product_key as product_key,
    s.sls_order_dt as order_date,
    s.sls_ship_dt as shipping_date,
    s.sls_due_dt as due_date,
    s.sls_sales as sales,
    s.sls_quantity as quantity,
    s.sls_price as price
from {{ ref('sales')}} s
left join {{ ref('dim_customers')}} c
on s.sls_cust_id = c.customer_id
left join {{ ref('dim_products')}} p
on s.sls_prd_key = p.product_number