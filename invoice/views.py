import json
from django.shortcuts import render,redirect
from django.http import JsonResponse

from invoice.models import Client, Invoice, Items, FromDetails
from django.views.decorators.csrf import csrf_exempt


# Create your views here.

def home(request):
    return render(request,'invoice-list.html')

def invoice(request):
    if Invoice.objects.exists():
        inv = Invoice.objects.last().id
        inv_id = 'INVSCR'+str(100000+inv)
    else:
        inv=0
        inv_id = 'INVSCR'+str(100000+inv)
    customers = Client.objects.all()
    admin_details = FromDetails.objects.all().last()
    items = Items.objects.all()
    context = {
        "invoice_id":inv_id,
        "customers":customers,
        "admin_details":admin_details,
        "items":items,
    }
    return render(request,'invoice.html',context)


#invoice ajax
@csrf_exempt
def customersearch(request):
    phone = request.POST['customerphone']
    if Client.objects.filter(phone=phone).exists():
        client = Client.objects.get(phone=phone)
    else :
        client = Client(phone=phone)
        client.save()
    data = {
        "name":client.name,
        "address":client.address,
        "city":client.city,
        "country":client.country,
        "zipcode":client.zipcode,
        "email":client.email,
    }
    return JsonResponse(data)


@csrf_exempt
def productsearch(request):
    pname = request.POST['product']
    if Items.objects.filter(description=pname).exists():
        item = Items.objects.get(description=pname)
        data = {
            "productexists":"itemexits",
            "itemname":item.description,
            "rate":item.rate,
            "taxable":item.is_taxable,
        }
        return JsonResponse(data)
    else :
        data = {
            "productexists":"itemdoesnotexits",
        }
        return JsonResponse(data)

@csrf_exempt
def saveinvoice(request):
    print(request.POST)
    data = json.loads(request.POST['data'])
    print(data)
    # data = request.POST['']
    data = {
        "fdsd":"sdas"
    }
    return JsonResponse(data)




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
    admin_details = FromDetails.objects.all().last()
    context = {
        "admin_details":admin_details,
    }
    return render(request,'settings.html',context)

