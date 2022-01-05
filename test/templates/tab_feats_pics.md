## Layer: {{ globals.vector_driver.name() }}
### Features:
| id          | loc        | pic1       | pic2       |
| ----------- | ---------- | ---------- | ---------- |
{% for feat in features %}| **{{ feat.id }}**  | ![feat {{ feat.id }}]({{ feat|image(width=299,height=300,dpi=200) }})  | ![feat {{ feat.id }}]({{ feat.attributes.pic|image(width=350,height=250,dpi=200) }})  |  ![feat {{ feat.id }}]({{ feat.attributes.pic|image(width=299,height=300,dpi=200) }}) |
{% endfor %}