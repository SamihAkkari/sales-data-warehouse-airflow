select 
    replace (cid, '-', '') as cid,
    {{ trim_clean_country('cntry') }} as cntry
from {{ source('bronze', 'loc') }}