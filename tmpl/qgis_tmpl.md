# globals

{% for var,value in globals.items() %}
**{{ var }}**: {{ value}}
{% endfor %}

# project {{ project.project_basename }}

{{ project.obj|prop('lastModified')|prop('toString',('yyyy-MM-dd')) }}

{% for var,value in project.items() %}
**{{ var }}**: {{ value}}
{% endfor %}

{% for layer in layers %}
![]({{ layer.extent|image(200,200,layer.obj)}})
{% for var,value in layer.items() %}
**{{ var }}**: {{ value}}
{% endfor %}

{% endfor %}