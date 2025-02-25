CACHE = {}
CURRENT_LOCATION = 'europe-west1'

{{ init_code }}


def run():
    user_project = '{{ project }}'
    bigfunction_dataset_location = 'EU'
    {% for name, value in arguments %}
    {{ name }} = {{ value | indent(4) }}
    {% endfor %}

    {{ code | indent(4) }}

result = run()
print(result)
