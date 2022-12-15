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



class Invoice(models.Model):
    invoice_number = models.CharField(max_length=50,null=True)
    client = models.ForeignKey(Client,on_delete=models.CASCADE,null=True)
    date = models.DateField(null=True)
    item_total = models.FloatField(default=0)
    tax_amount = models.FloatField(default=0)
    grand_total = models.FloatField(default=0)
    amount_paid = models.FloatField(default=0)
    note = models.CharField(max_length=2000,null=True)

    def __str__(self):
        return str(self.invoice_number)

    def getdetails(self):
        return InvoiceItems.objects.filter(invoice=self)


class InvoiceItems(models.Model):
    invoice = models.ForeignKey(Invoice,on_delete=models.CASCADE,null=True)
    item = models.ForeignKey(Items,on_delete=models.CASCADE,null=True)
    quantity = models.IntegerField(default=1)
    total = models.FloatField(default=0)
    tax = models.FloatField(default=0)
    # tax_applied = models.BooleanField(default=True)
    itemtotal = models.FloatField(default=0)

    def __str__(self):
        return str(self.invoice)


class BillPayment(models.Model):
    invoice = models.ForeignKey(Invoice,on_delete=models.CASCADE,null=True)
    amount = models.FloatField(default=0)
    date = models.DateField(null=True)
    balance = models.FloatField(default=0)

    def __str__(self):
        return str(self.invoice)



