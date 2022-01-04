# report progetto {{ globals.project.fileName() }}
#### Location: {{ globals.project.absoluteFilePath() }}
#### Variables:
{% for key,var in globals.vars.items() %} {{ key }} {{ var }}
{% endfor %}

![]( {{ globals|image(400,400) }} )


| icon                           | f1   | f2   | f3   | f4   |
| ------------------------------ | ---- | ---- | ---- | ---- |
{% for layer in layers %} | ![]({{ layer|image(200,200)}}) | {{ layer.name }} | {{ layer.obj.crs().authid() }} |{{ layer.source }}|{{ layer.type }}     |
{% endfor %}
