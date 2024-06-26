from django.db import models


class Subject(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name
