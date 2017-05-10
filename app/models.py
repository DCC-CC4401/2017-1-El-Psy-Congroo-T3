from django.db import models


# Create your models here.

class Seller(models.Model):
    name = models.CharField(max_length=20, default='')
    active = models.BooleanField(default=False)
    fixed = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name
