{% macro trim_clean_gender(column) %}
    case 
        when upper(trim({{column}})) in ('M', 'MALE') then 'Male' 
	    when upper(trim({{column}})) in ('F', 'FEMALE') then 'Female'
	    else 'Unknown'
    end 
{% endmacro %}

{% macro trim_clean_country(column) %}
    case 
        when trim({{column}}) = 'DE' then 'Germany'
        when trim({{column}}) in ('US', 'USA') then 'United States'
        when trim({{column}}) = '' or {{column}} is null then 'Unkown'
        else trim({{column}})
    end 
{% endmacro %}

{% macro cast_int_to_date(column)%}
    cast(case 
            when length(cast({{column}} as text)) = 8 then to_date(cast({{column}} as text), 'YYYYMMDD')
            else null
        end as date
            )
{% endmacro %}