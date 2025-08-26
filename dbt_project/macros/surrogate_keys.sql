{% macro generate_surrogate_key(column) %}
    row_number() over (order by {{column}})
{% endmacro %}