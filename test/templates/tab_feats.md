## Layer: {{ globals.vector_driver.name() }}
### Features:
| id          | loc        | desc       |
| ----------- | ---------- | ---------- |
{% for feat in features %}| **{{ feat.id }}**  | ![feat {{ feat.id }}]({{ feat|image(width=399,height=400,dpi=300) }})  | {% for k,v in feat.attributes.items() %}*{{k}}: {{v}}*<br/>{% endfor %}   |
{% endfor %}