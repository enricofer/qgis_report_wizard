{% for k,layout in layouts.items() %}{% if layout.atlas %}
### Atlas: {{ layout.atlas.name() }}
| name          | pic        |
| ------------- | ---------- |
{% for f in layout.atlas.getFeatures() %}| **{{ f.id() }}**  | ![atlas {{ f.id() }}]({{ layout|image(width=300,height=200,dpi=200,atlas=f.id()) }})  |
{% endfor %}{% endif %}
{% endfor %}