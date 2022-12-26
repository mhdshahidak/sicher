import datetime
import json
from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout
from . import sms
from twilio.rest import Client



from invoice.models import BillPayment, ClientDetails, Invoice, InvoiceItems, Items, FromDetails
from django.views.decorators.csrf import csrf_exempt


# Create your views here.

def loginPage(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)
        if user is not None :
            auth_login(request,user)
            return redirect("invoice:home")
        else :
            context = {
                "msg":1,
            }
            return render(request,'login.html',context)
    context = {
        "msg":0
    }
    return render(request,'login.html',context)

def logoutView(request):
    logout(request)
    return redirect("invoice:loginpage")


@login_required(login_url="/login-page/")
def home(request):
    invoices = Invoice.objects.all()
    context = {
        "invoices" : invoices,
    }
    return render(request,'invoice-list.html',context)

@login_required(login_url="/login-page/")
def invoice(request):
    if Invoice.objects.exists():
        inv = Invoice.objects.last().id
        inv_id = 'INVSCR'+str(100000+inv)
    else:
        inv=0
        inv_id = 'INVSCR'+str(100000+inv)
    customers = ClientDetails.objects.all()
    admin_details = FromDetails.objects.all().last()
    items = Items.objects.all()
    context = {
        "invoice_id":inv_id,
        "customers":customers,
        "admin_details":admin_details,
        "items":items,
    }
    return render(request,'invoice.html',context)

@login_required(login_url="/login-page/")
def bill(request,id):
    invoice = Invoice.objects.get(id=id)
    admin_details = FromDetails.objects.all().last()
    context = {
        "invoice":invoice,
        "admin_details":admin_details,
    }
    return render(request,'bill.html', context)

@login_required(login_url="/login-page/")
def payment(request,id):
    invoice = Invoice.objects.get(id=id)
    balance = invoice.grand_total - invoice.amount_paid
    if invoice.grand_total <= invoice.amount_paid :
        invoice.status = "Paid"
        invoice.save()
    elif balance <= 0 :
        invoice.status = "Paid"
        invoice.save()
    else :
        pass
    history = BillPayment.objects.filter(invoice=invoice)
    if request.method == "POST":
        amount = request.POST['amount']
        to_date = datetime.date.today()
        balance_after_pay = balance - int(amount)
        new_pay = BillPayment(invoice=invoice,amount=amount,date=to_date,balance=balance_after_pay)
        new_pay.save()
        invoice.amount_paid = invoice.amount_paid + int(amount)
        invoice.save()
        return redirect('/payment/'+str(id))
    context = {
        "invoice":invoice,
        "history":history,
        "balance":balance,
    }
    return render(request,'payment-page.html',context)



def msgsending(request,id):
    client = Client(sms.TWILIO_ACCOUNT_SID, sms.TWILIO_AUTH_TOKEN)

    message = client.messages.create(
            messaging_service_sid='MG859803b3a99454fddcd325a8546356a0', 
            body=f'Pay your Bill here https://rzp.io/l/ruYYyLXsJ3 ',   
            to='+917510661741'
        )
    return redirect('/bill/'+str(id))


#invoice ajax
@csrf_exempt
def customersearch(request):
    phone = request.POST['customerphone']
    if ClientDetails.objects.filter(phone=phone).exists():
        client = ClientDetails.objects.get(phone=phone)
    else :
        client = ClientDetails(phone=phone)
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
    data = json.loads(request.POST['data'])
    try :
        basic_datas = data[0]
        invoice_number = basic_datas['invoicenumber']
        customer_phone = basic_datas['customerphone']
        invoice_date = basic_datas['invoicedate']
        subtotall = basic_datas['subtotall']
        gtotal = basic_datas['gtotal']
        notes = basic_datas['note']
        # print(invoice_date,"#"*10)
        if invoice_date == "" :
            date = datetime.date.today()
        else :
            date = invoice_date
        customer = ClientDetails.objects.get(phone=customer_phone)
        if notes == "" :
            note = "Notes Does not added"
        else :
            note = notes
        new_invoice = Invoice(invoice_number=invoice_number,client=customer,date=date,item_total=subtotall,grand_total=gtotal,note=note,status="Due")
        new_invoice.save()

        for i in data[1:]:
            item_name = i['itemname']
            quantity = i['qty']
            itemtotal = i['itemtotal']
            itemtaxtotal = i['itemtaxtotal']
            checkvalue = i['checkvalue']
            if Items.objects.filter(description=item_name).exists():
                product = Items.objects.get(description=item_name)
            else :
                product = Items(description=item_name)
                product.save()
            tax = int(itemtaxtotal) - int(itemtotal)
            new_invoice_item = InvoiceItems(invoice=new_invoice,item=product,quantity=quantity,total=itemtotal,itemtotal=itemtaxtotal,tax=tax)
            new_invoice_item.save()
            msg = "Invoice saved successfully"
    except :
        msg = "Somthing went Wrong Please try again"
        pass
    # data = request.POST['']
    data = {
        "msg": msg,
    }
    return JsonResponse(data)



@login_required(login_url="/login-page/")
def estimate_list(request):
    invoices = Invoice.objects.all()
    context = {
        "invoices" : invoices,
    }
    return render(request,'invoice-details.html',context)

@login_required(login_url="/login-page/")
def clients(request):
    clients = ClientDetails.objects.all()
    context = {
        "clients":clients,
    }
    return render(request,'client-list.html',context)

@login_required(login_url="/login-page/")
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
        if not ClientDetails.objects.filter(phone=phone).exists():
            new_client = ClientDetails(name=name,email=email,phone=phone,city=city,country=state,address=address,zipcode=zipcode)
            new_client.save()
            return redirect('invoice:clients')
        else :
            return render(request,'add-customer.html')
    return render(request,'add-customer.html')

@login_required(login_url="/login-page/")
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

@login_required(login_url="/login-page/")
def edit_items(request,id):
    item = Items.objects.get(id=id)
    if request.method == "POST":
        name = request.POST['name']
        price = request.POST['price']
        aditional_details = request.POST['aditional_details']
        # try :
        #     taxable = request.POST['taxable']
            
        #     Items.objects.filter(id=id).update(description=name,rate=price,aditional_details=aditional_details)
        #     return redirect("invoice:items")
        # except :
        #     Items.objects.filter(id=id).update(description=name,rate=price,aditional_details=aditional_details,is_taxable=False)
        #     return redirect("invoice:items")
        Items.objects.filter(id=id).update(description=name,rate=price,aditional_details=aditional_details)
        return redirect("invoice:items")
        
    context = {
        "item" : item,
    }
    return render(request,'edit-items.html',context)


@login_required(login_url="/login-page/")
def edit_customer(request,id):
    customer = ClientDetails.objects.get(id=id)
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        city = request.POST['city']
        state = request.POST['state']
        address = request.POST['address']
        zipcode = request.POST['zipcode']
        ClientDetails.objects.filter(id=id).update(name=name,email=email,phone=phone,city=city,country=state,address=address,zipcode=zipcode)
        return redirect('invoice:clients')
    context = {
        "customer" : customer,
    }
    return render(request,'edit-customer.html', context)


@csrf_exempt
def delete_item(request):
    id = request.POST['id']
    product = Items.objects.get(id=id)
    product.delete()
    return JsonResponse({"msg":"ggg"})


@csrf_exempt
def deleteClient(request):
    id = request.POST['id']
    client = ClientDetails.objects.get(id=id)
    client.delete()
    return JsonResponse({"msg":"ggg"})

@csrf_exempt
def deleteinvoice(request):
    id = request.POST['id']
    invoice = Invoice.objects.get(id=id)
    invoice.delete()
    return JsonResponse({"msg":"ggg"})


@login_required(login_url="/login-page/")
def settings(request):
    admin_details = FromDetails.objects.all().last()
    context = {
        "admin_details":admin_details,
    }
    return render(request,'settings.html',context)

