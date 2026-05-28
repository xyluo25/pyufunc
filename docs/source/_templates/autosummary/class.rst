{{ fullname | escape | underline}}

.. currentmodule:: {{ module }}

.. py:class:: {{ objname }}
{% set public_methods = methods | reject("equalto", "__init__") | list %}
{% if public_methods %}

.. rubric:: {{ _('Methods') }}

.. autosummary::
{% for item in public_methods %}
   ~{{ name }}.{{ item }}
{% endfor %}
{% endif %}
{% if attributes %}

.. rubric:: {{ _('Attributes') }}

.. autosummary::
{% for item in attributes %}
   ~{{ name }}.{{ item }}
{% endfor %}
{% endif %}
