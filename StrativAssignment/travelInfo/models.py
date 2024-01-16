from django.db import models

class District(models.Model):
    id = models.CharField(max_length=5, primary_key=True)
    division_id = models.CharField(max_length=5)
    name = models.CharField(max_length=100)
    bn_name = models.CharField(max_length=100)
    lat = models.CharField(max_length=20)
    long = models.CharField(max_length=20)

    def __str__(self):
        return self.name
