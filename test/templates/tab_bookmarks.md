| name                           | Layer thumb   | 
| ------------------------------ | ------------- |
{% for key,bk_def in globals.bookmarks.items() %} | **{{bk_def.name}}**<br/>*type:{% if bk_def.is_user_bookmark %}USER{% else %}PROJECT{% endif %}* | ![]({{ globals|image(300,300,extent=bk_def.extent) }} ) |
{% endfor %}