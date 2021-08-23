# report progetto {{ project.obj|prop('baseName')}}
#### Location: {{ project.obj|prop('absoluteFilePath')}}
#### Location: {{ project.obj|prop('customVariables')}}

| icon                           | f1   | f2   | f3   | f4   |
| ------------------------------ | ---- | ---- | ---- | ---- |
{% for layer in layers %} | ![]({{ layer.obj|prop('extent')|image(600,600,[layer.obj])}}) | {{ layer.obj|prop("name") }} | {{ layer.obj|prop('crs')|prop('authid')}} |{{ layer.obj|prop('source')}}|{{ layer.obj|prop('type')}}     |
{% endfor %}