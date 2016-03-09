Django Model Mapper
===================

#Usage

1. Choose a low-format parser
-----------------------------
Imagine you want to populate your DB from the following XML:
```xml
<root>
    <row id="1">
        <title>Meaningful string</title>
    </row>
</root>
```

Just pick the ModelAwareXMLParser. It converts even such an ambiguous
data format like xml to a native python representation nicely.
Notice that attributes will be mapped to a properties with names prefixed by @ char.


```python
    {
        '@id': '1',
        'title': 'Meaningful string'
    }
```

2. Create mappers for your models
----------------------------------
Assuming you have a model like this:
```python

from django.db import models

class TestModel(models.Model):
    id = models.IntegerField()
    title = models.CharField(max_length=8)
```

```python
from model_mapper import ModelMapper, FieldBinding

class TestMapper(ModelMapper):
    class meta:
        model = TestModel

    id = FieldBinding('@id')
    title = FieldBinding('title')
```

Mappers will extract the data from the python objects and create a model
instances. They do not do type casting, cause its ORM's responsibility.
If you need to handle a many-to many relationships, specify save_m2m
method for the mapper class and do it manually.

```
    def save_m2m(self, inst, m2m_data):
        for tag in m2m_data['tags']:
            inst.tags.add(Tag.objects.get_or_create(value=tag)[0])
```

2. Run the chosen parser with your mappers
```
    p = ModelAwareXMLParser()
    p.register_mapper('event', EventMapper())
    p.register_mapper('place', PlaceMapper())
    p.register_mapper('session', ScheduleMapper())
    p.run(feed)
```
