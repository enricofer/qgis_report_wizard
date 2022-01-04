### Layouts:
| name          | pic        |
| ------------- | ---------- |
{% for k,l in layouts.items() %}| **{{ l.name }}**  | ![layout {{ l.name }}]({{ l|image(width=600,height=400,dpi=200) }})  |
{% endfor %}