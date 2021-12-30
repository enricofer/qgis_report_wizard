# test table 1

| C1                                           | C2                  | C3                 | C4                           |
| :---- | ------------------- | ---------------------------- | ---------------------------- |
{% for feat in features %} {{ feat.id }}| ![]({{ feat|image(100,100,around_border=0.2) }}) | {{ feat.attributes.pic|image(150,150) }} | {% for attr_name,attr_val in feature.attributes.items() %} **{{ attr_name }}: **{{attr_value}}<br/>{% endfor %}|
{% endfor %}

# end table
