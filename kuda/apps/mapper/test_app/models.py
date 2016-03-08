from django.db import models


class TestModel(models.Model):
    class Meta:
        db_table = 'test_app_testmodel'

    field1 = models.IntegerField(null=True)
    field2 = models.CharField(max_length=8)
