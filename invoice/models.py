from django.db import models

# Create your models here.


class FromDetails(models.Model):
    name = models.CharField(max_length=50,null=True)
    phone = models.CharField(max_length=20,null=True)
    email = models.CharField(max_length=50,null=True)
    website = models.CharField(max_length=50,null=True)
    address = models.CharField(max_length=100,null=True)
    district = models.CharField(max_length=50,null=True)
    state = models.CharField(max_length=25,null=True)
    pincode = models.CharField(max_length=15,null=True)

    class Meta:
        verbose_name_plural = ("Main Admin")

    def __str__(self):
        return str(self.phone)


class Client(models.Model):
    name = models.CharField(max_length=200,null=True)
    email = models.CharField(max_length=200,null=True)
    address = models.CharField(max_length=500,null=True)
    city = models.CharField(max_length=500,null=True)
    country = models.CharField(max_length=50,null=True)
    zipcode = models.CharField(max_length=20,null=True)
    phone = models.CharField(max_length=20,unique=True,null=True)

    class Meta:
        verbose_name_plural = ("Client")

    def __str__(self):
        return str(self.name)


class Items(models.Model):
    description = models.CharField(max_length=50,null=True)
    rate = models.FloatField(default=0,null=True)
    aditional_details = models.CharField(max_length=500,null=True)
    is_taxable = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)


    class Meta:
        verbose_name_plural = ("Items")

    def __str__(self):
        return str(self.description)


