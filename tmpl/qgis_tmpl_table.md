# test table 1

| img                                           | fid                  | COD_ISTAT                 | ID_PARCOMM                           |
| :---- | ------------------- | ---------------------------- | ---------------------------- |
{% for feature in layer %}| ![]({{ feature.geom|image(100,100,around_border=0.2) }}) | `{{ feature.fid }}` | **{{ feature.COD_ISTAT }}** | **{{ feature.ID_PARCOMM }}** |
{% endfor %}

# end table