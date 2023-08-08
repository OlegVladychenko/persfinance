from django.db import models

# Create your models here.

class Document(models.Model):
    type = models.IntegerField()
    date = models.DateTimeField(auto_now=True)
    sum = models.DecimalField(max_digits=10, decimal_places=2)
    counterparty_id = models.ForeignKey('Сounterparty', on_delete=models.PROTECT, blank=True)
    category_id = models.ForeignKey('Category', on_delete=models.PROTECT, blank=True)
    сurrencie_id = models.ForeignKey('Currencies', on_delete=models.PROTECT, blank=True)
    active = models.BooleanField(default=True)


class Сounterparty(models.Model):
    name = models.CharField(max_length=255)
    comment = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=255)
    comment = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name

class Currencies(models.Model):
    code = models.CharField(max_length=3, db_index=True, primary_key=True)
    name = models.CharField(max_length=100)
    full_name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class TypeDebit(models.Model):
    name = models.CharField(max_length=255)
    comment = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name

class TypeCredit(models.Model):
    name = models.CharField(max_length=255)
    comment = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name

class MoneyAccount(models.Model):
    name = models.CharField(max_length=255)
    type = models.IntegerField() # 0- cash 1- Bank account
    сurrencie_id = models.ForeignKey('Currencies', on_delete=models.PROTECT)
    comment = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name