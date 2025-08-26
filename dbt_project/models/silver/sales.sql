
with flagged as (
SELECT
	*,
	(sls_sales IS NULL OR sls_sales = 0) AS bad_sales,
	(sls_quantity IS NULL OR sls_quantity = 0) AS bad_quantity,
	(sls_price IS NULL OR sls_price = 0) AS bad_price,
	(
		sls_sales IS NOT NULL AND sls_sales <> 0
		AND sls_quantity IS NOT NULL AND sls_quantity <> 0
		AND sls_price IS NOT NULL AND sls_price <> 0
		AND ABS(sls_sales * sls_quantity - sls_price) > 0.01
	) AS inconsistent
FROM {{ source('bronze', 'sales') }}
)

SELECT
	sls_ord_num,
	sls_prd_key,
	sls_cust_id,
	{{ cast_int_to_date('sls_order_dt') }} as sls_order_dt,
    {{ cast_int_to_date('sls_ship_dt') }} as sls_ship_dt,
    {{ cast_int_to_date('sls_due_dt') }} as sls_due_dt,
    CASE 
        WHEN bad_sales AND NOT bad_quantity AND NOT bad_price THEN sls_price / sls_quantity
        ELSE sls_sales
    END AS sls_sales,
    CASE 
        WHEN bad_quantity AND NOT bad_sales AND NOT bad_price THEN sls_price / sls_sales
        ELSE sls_quantity
    END AS sls_quantity,
    CASE 
        WHEN bad_price AND NOT bad_sales AND NOT bad_quantity THEN sls_sales * sls_quantity
		WHEN inconsistent THEN sls_sales * sls_quantity
        ELSE sls_price
	END AS sls_price
FROM flagged