from django.urls import path
from . import views

app_name = 'invoice'

urlpatterns = [
    path('',views.home, name='home'),
    path('invoice',views.invoice, name='invoice'),
    path('estimates',views.estimate_list, name='estimates'),
    path('clients',views.clients, name='clients'),
    path('add-clients',views.addClients, name='addClients'),
    path('items',views.items, name='items'),
    path('edit-items/<int:id>',views.edit_items, name="edit_items"),
    path('edit-customer/<int:id>',views.edit_customer, name="edit_customer"),
    path('bill/<int:id>',views.bill, name="bill"),

    path('settings',views.settings, name='settings'),

    #ajax
    path('customersearch/',views.customersearch, name='customersearch'),
    path('productsearch/',views.productsearch, name='productsearch'),
    path('saveinvoice/',views.saveinvoice, name="saveinvoice"),
    path('deleteitems/',views.delete_item, name="delete_item"),
    path('deleteclient/',views.deleteClient, name="deleteClient"),

]
