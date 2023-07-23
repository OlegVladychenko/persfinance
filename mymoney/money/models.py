from django.db import models

# Create your models here.

class Document(models.Model):
    type = models.IntegerField()
    date = models.DateTimeField(auto_now=True)
    sum = models.DecimalField(max_digits=10, decimal_places=2)
    counterparty_id = models.ForeignKey('Сounterparty', on_delete=models.PROTECT, blank=True)
    category_id = models.ForeignKey('Category', on_delete=models.PROTECT, blank=True)
    active = models.BooleanField(default=True)


class Сounterparty(models.Model):
    name = models.CharField(max_length=255)
    comment = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=255)
    comment = models.CharField(max_length=255)

    def __str__(self):
        return self.name