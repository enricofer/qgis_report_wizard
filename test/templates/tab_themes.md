| name                           | Layer thumb   | 
| ------------------------------ | ------------- |
{% for theme in globals.themes %} | **{{theme}}** | ![]({{ globals|image(300,300,theme=theme)}}) |
{% endfor %}| **default** | ![]({{ globals|image(300,300,theme="")}}) |