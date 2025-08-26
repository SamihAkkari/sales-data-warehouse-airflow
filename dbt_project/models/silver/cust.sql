select 
    case 
        when cid like 'NAS%' then substring(cid, 4, length(cid))
        else cid
    end as cid,
    case 
        when cast(bdate as date) > current_date then null
        else cast(bdate as date)
    end as bdate,
    {{ trim_clean_gender('gen') }} as gen
from {{ source('bronze', 'cust') }}