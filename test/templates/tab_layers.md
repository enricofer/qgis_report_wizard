| Layer thumb                     | details   | fields   |
| ------------------------------ | --------- | -------- |
{% for layer in layers %} | ![]({{ layer|image(300,300)}})<br/>layer|image(150,150|extent=[759723,5035882,763553,5038034])}}) | NAME: {{ layer.name }} <br/>CRS: {{ layer.obj.crs().authid() }}<br/>TYPE:{{ layer.layerType }}     | {%if layer|isVector() %}{% for f in layer.fields %}{{ f }}<br/>{% endfor %}{% else %}**no fields**{% endif %} |
{% endfor %}