from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request,'invoice-list.html')

def invoice(request):
    return render(request,'invoice.html')

def estimate_list(request):
    return render(request,'estimate-list.html')

def clients(request):
    return render(request,'client-list.html')

def items(request):
    return render(request,'items.html')

def settings(request):
    return render(request,'settings.html')

