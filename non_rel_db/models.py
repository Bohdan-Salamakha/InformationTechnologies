from django.db import models


class Employee(models.Model):
    name = models.CharField(max_length=128)
    position = models.CharField(max_length=128)
    salary = models.IntegerField()

    class Meta:
        managed = False
