from django.urls import path
from . import views

app_name = 'invoice'

urlpatterns = [
    path('',views.home, name='home'),
    path('invoice',views.invoice, name='invoice'),
    path('estimates',views.estimate_list, name='estimates'),
    path('clients',views.clients, name='clients'),
    path('items',views.items, name='items'),
    path('settings',views.settings, name='settings'),
]