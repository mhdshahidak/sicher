from django.shortcuts import render,redirect

from invoice.models import Client, Items

# Create your views here.

def home(request):
    return render(request,'invoice-list.html')

def invoice(request):
    return render(request,'invoice.html')

def estimate_list(request):
    return render(request,'estimate-list.html')

def clients(request):
    clients = Client.objects.all()
    context = {
        "clients":clients,
    }
    return render(request,'client-list.html',context)

def addClients(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        city = request.POST['city']
        state = request.POST['state']
        address = request.POST['address']
        zipcode = request.POST['zipcode']
        # name = request.POST['name']
        if not Client.objects.filter(phone=phone).exists():
            new_client = Client(name=name,email=email,phone=phone,city=city,country=state,address=address,zipcode=zipcode)
            new_client.save()
            return redirect('invoice:clients')
        else :
            return render(request,'add-customer.html')
    return render(request,'add-customer.html')

def items(request):
    all_items = Items.objects.filter(is_active = True)
    if request.method == "POST":
        name = request.POST['name']
        price = request.POST['price']
        aditional_details = request.POST['aditional_details']
        if not Items.objects.filter(description=name).exists():
            try :
                taxable = request.POST['taxable']
                new_item = Items(description=name,rate=price,aditional_details=aditional_details)
                new_item.save()
                return redirect("invoice:items")
            except :
                new_item = Items(description=name,rate=price,aditional_details=aditional_details,is_taxable=False)
                new_item.save()
                return redirect("invoice:items")
        else:
            pass
    context = {
        "all_items":all_items,
    }
    return render(request,'items.html',context)

def settings(request):
    return render(request,'settings.html')

