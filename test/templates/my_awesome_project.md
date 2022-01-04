# IN MY AWESOME QGIS PROJECT… 

### THE CURRENT MAP CANVAS IS:
![]( {{ globals|image(600,600) }} )

### BUT YOU CAN CAN GET IT AT A SPECIFIED SCALE (1:10000):
![]( {{ globals|image(400,400,scale_denominator=10000) }} )

### OR FOR A SPECIFIED LOCATION AND SCALE (5000):
![]( {{ globals|image(800,400,scale_denominator=5000,center=globals.mapCanvas.extent().center() ) }} )

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



#### Location: {{ globals.project.absoluteFilePath() }}
#### Variables:
{% for key,var in globals.vars.items() %} {{ key }} {{ var }}
{% endfor %}

![]( {{ globals|image(400,400) }} )


| icon                           | f1   | f2   | f3   | f4   |
| ------------------------------ | ---- | ---- | ---- | ---- |
{% for layer in layers %} | ![]({{ layer|image(200,200)}}) | {{ layer.name }} | {{ layer.obj.crs().authid() }} |{{ layer.source }}|{{ layer.layerType }}     |
{% endfor %}
