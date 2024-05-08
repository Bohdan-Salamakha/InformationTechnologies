from django.db import models


class Employee(models.Model):
    name = models.CharField(max_length=128)
    position = models.CharField(max_length=128)
    salary = models.IntegerField()

    class Meta:
        managed = False


class Student(models.Model):
    id = models.CharField(max_length=256, primary_key=True)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    enrollment_year = models.IntegerField()

    class Meta:
        managed = False
