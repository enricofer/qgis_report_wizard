| Layer thumb                     | details   | fields   |
| ------------------------------ | --------- | -------- |
{% for layer in layers %} | ![]({{ layer|image(300,300)}}) | NAME: {{ layer.name }} <br/>CRS: {{ layer.obj.crs().authid() }}<br/>TYPE:{{ layer.layerType }}     | {%if layer|isVector() %}{% for f in layer.fields %}{{ f }}<br/>{% endfor %}{% else %}**no fields**{% endif %} |
{% endfor %}