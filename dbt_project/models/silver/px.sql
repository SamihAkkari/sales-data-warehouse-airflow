select 
    id,
    cat,
    subcat,
    maintenance
from {{ source('bronze', 'px') }}