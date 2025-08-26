
select 
{{generate_surrogate_key('c.cst_id')}} as customer_key,
c.cst_id as customer_id,
c.cst_key as customer_number,
c.cst_firstname as firstname,
c.cst_lastname as lastname,
c.cst_marital_status as marital_status,
case 
	when c.cst_gndr = 'Unknown' then cu.gen
	else c.cst_gndr
end as gender,
cu.bdate as birthdate,
l.cntry as country
from {{ ref('customers') }} c
left join {{ ref('cust') }} cu
on c.cst_key = cu.cid
left join {{ ref('loc') }} l
on c.cst_key = l.cid