from django.db import models

# Create your models here.

class Car(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(null=True, blank=True)
    color = models.CharField(max_length=20)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(null=True, blank=True)
    # inventory = models.IntegerField()
    # last_update = models.DateTimeField(auto_now=True)
    # collection = models.ForeignKey(Collection, on_delete=models.PROTECT, related_name='products')
    # promotions = models.ManyToManyField(Promotion)
