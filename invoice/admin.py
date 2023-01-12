from django.contrib import admin
from . models import *

# Register your models here.
admin.site.register(FromDetails)

class ClientDetailsAdmin(admin.ModelAdmin):
    list_display = ('name','email','phone')
    search_fields=('phone',)
admin.site.register(ClientDetails,ClientDetailsAdmin)


class ItemsAdmin(admin.ModelAdmin):
    list_display = ('description',)
    search_fields=('description',)
admin.site.register(Items,ItemsAdmin)

class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_number','client','date')
    search_fields=('invoice_number',)
admin.site.register(Invoice,InvoiceAdmin)


class InvoiceItemsAdmin(admin.ModelAdmin):
    list_display = ('invoice','item','itemtotal')
    search_fields=('invoice',)
admin.site.register(InvoiceItems,InvoiceItemsAdmin)

admin.site.register(BillPayment)
