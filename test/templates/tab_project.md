# ALL ABOUT MY AWESOME QGIS PROJECT… 

### THE CURRENT MAP CANVAS IS:
![]( {{ globals|image(600,600) }} )

### BUT YOU CAN CAN GET IN A DIFFERENT SIZE:
![]( {{ globals|image(400,400) }} )

### OR FOR A SPECIFIED LOCATION AND SIZE:
![]( {{ globals|image(800,400,center=globals.mapCanvas.extent().center() ) }} )

The plugin provides to the template four variables populated with data from current project and related elements:
- `globals` 	information about project and current visualization on map canvas
- `layers`   	information about loaded layers
- `features`  attributes and geometries about a specified vector layer
- `layouts`   information about current print layouts



## globals variable

in the global variable are loaded general informations about the current project, accessible by the following keys:

| key         | desc                                                         | tag                                          | result                                                       |
| ----------- | ------------------------------------------------------------ | -------------------------------------------- | ------------------------------------------------------------ |
| `project`   | The [QgsProject](https://qgis.org/pyqgis/3.0/core/Project/QgsProject.html) object instance | {% raw %}`{{globals.project }}`{% endraw %}  | {{ globals.project }}<br/>{{ globals.project.baseName() }}             |
| `mapCanvas` | The [QgsMapCanvas](https://qgis.org/pyqgis/3.2/gui/Map/QgsMapCanvas.html) object instance | {% raw %}`{{globals.mapCanvas}}`{% endraw %} | {{ globals.mapCanvas }}<br />{{ globals.mapCanvas.layerCount() }}<br />{{ globals.mapCanvas.scale() }} |
| `vars`      | A dictionary with the current global variables               | {% raw %}`{{globals.vars}}`{% endraw %}      | {{ globals.vars }}                                           |
| `bbox`       | An array with the current map canvas extent [xmin,ymin,xmax,ymax] | {% raw %}`{{globals.bbox}}`{% endraw %}       | {{ globals.box}}                                             |
| `themes`    | A list of user defined legend themes                         | {% raw %}`{{globals.themes}}`{% endraw %}    |                                                              |
| `bookmarks` | A list of user defined and project bookmarks                 | {% raw %}`{{globals.bookmarks}}`{% endraw %} | {{ globals.bookmarks }}                                      |
| ....        | Other information can be retrieved accessing project and mapCanvas objects |                                              |                                                              |

### globals keys:

| key         | desc       |
| ----------- | ---------- |
{% for key,value in globals.items() %}| **{{ key }}**  | {% if value is iterable and value is not string %}{% if value is mapping %}{% for k,v in value.items() %}*{{k}}: {{v}}*<br/>{% endfor %}{% else %}{% for i in value %}*{{i}}*<br/>{% endfor %}{% endif %}{% else %}*{{ value }}*{% endif %}  |
{% endfor %}

### layouts keys:
{% set l = layouts.values()|first %}
| key         | desc       |
| ----------- | ---------- |
{% for key,value in l.items() %}| **{{ key }}**  | {% if value is iterable and value is not string %}{% if value is mapping %}{% for k,v in value.items() %}*{{k}}: {{v}}*<br/>{% endfor %}{% else %}{% for i in value %}*{{i}}*<br/>{% endfor %}{% endif %}{% else %}*{{ value }}*{% endif %}  |
{% endfor %}

### layers keys:
{% set l = layers|first %}
| key         | desc       |
| ----------- | ---------- |
{% for key,value in l.items() %}| **{{ key }}**  | {% if value is iterable and value is not string %}{% if value is mapping %}{% for k,v in value.items() %}*{{k}}: {{v}}*<br/>{% endfor %}{% else %}{% for i in value %}*{{i}}*<br/>{% endfor %}{% endif %}{% else %}*{{ value }}*{% endif %}  |
{% endfor %}

{% if features %}
### features keys:
{% set l = features|first %}
| key         | desc       |
| ----------- | ---------- |
{% for key,value in l.items() %}| **{{ key }}**  | {% if value is iterable and value is not string %}{% if value is mapping %}{% for k,v in value.items() %}*{{k}}: {{v}}*<br/>{% endfor %}{% else %}{% for i in value %}*{{i}}*<br/>{% endfor %}{% endif %}{% else %}*{{ value }}*{% endif %}  |
{% endfor %}
{% endif %} 