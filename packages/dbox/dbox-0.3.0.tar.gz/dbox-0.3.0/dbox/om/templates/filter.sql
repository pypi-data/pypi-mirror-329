select *
from (
  {{ source | indent(2) }}
)
{% if conditions %}
where
  {{+ conditions | join('\n  and ') }}
{% endif %}