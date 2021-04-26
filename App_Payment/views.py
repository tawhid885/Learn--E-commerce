from django.shortcuts import render,redirect,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse

#Models and Forms
from App_Payment.models import BillingAddress
from App_Payment.forms import BillingForm
from App_Order.models import Order,Cart


#For Payment
import requests
from sslcommerz_python.payment import SSLCSession
from decimal import Decimal
import socket
from django.views.decorators.csrf import csrf_exempt

@login_required
def payment(request):
    saved_address = BillingAddress.objects.get_or_create(user = request.user)[0]

    if not saved_address.is_fully_filled():
        messages.info(request,f"Please complete shipping address!")
        return redirect("App_Payment:checkout")
    
    if not request.user.profile.is_fully_filled():
        messages.info(request,f"Please complete your profile!")
        return redirect("App_Login:profile")
    
    store_id ='mybus608700db601ed'
    API_key = 'mybus608700db601ed@ssl'

    status_url = request.build_absolute_uri(reverse("App_Payment:complete"))
    # print(status_url)
    
    mypayment = SSLCSession(sslc_is_sandbox=True, sslc_store_id=store_id, sslc_store_pass=API_key)
    mypayment.set_urls(success_url=status_url, fail_url=status_url, cancel_url=status_url, ipn_url=status_url)

    order_qs = Order.objects.filter(user = request.user, ordered=False)
    order_item = order_qs[0].orderitems.all()
    order_item_count = order_qs[0].orderitems.count()
    order_total = order_qs[0].get_total()

    mypayment.set_product_integration(total_amount=Decimal(order_total), currency='BDT', product_category='Mixed', product_name=order_item, num_of_item=order_item_count, shipping_method='Courier', product_profile='None')



    mypayment.set_customer_info(name=request.user.profile.full_name, email=request.user.email, address1=request.user.profile.address, address2=request.user.profile.address, city='Dhaka', postcode=request.user.profile.zipcode, country='Bangladesh', phone=request.user.profile.phone)

    mypayment.set_shipping_info(shipping_to=request.user.profile.full_name, address=saved_address.address, city=saved_address.city, postcode=saved_address.zipcode, country=saved_address.country)

    response_data = mypayment.init_payment()
    # print(response_data)
    
    # return render(request, 'App_Payment/payment.html',context={})
    return redirect(response_data['GatewayPageURL'])


@csrf_exempt
def complete(request):
    if request.method == 'POST' or request.method == 'post':
        payment_data = request.POST
        status = payment_data['status']
        

        if status == 'VALID':
            tran_id = payment_data['tran_id']
            val_id = payment_data['val_id']
            bank_tran_id = payment_data['bank_tran_id']
            messages.success(request,f"Your payment completed successfully!")
            return HttpResponseRedirect(reverse("App_Payment:purchase",kwargs={'val_id':val_id,'tran_id':tran_id}))
        
        elif status == 'FAILED':
            messages.warning(request,f"Your payment failed! Please try again! Page will be redirected soon!")
        

    return render(request,"App_Payment/complete.html",context={})


@login_required
def purchase(request,val_id, tran_id):
    order_qs = Order.objects.filter(user = request.user, ordered=False)
    order = order_qs[0]

    orderId = tran_id
    order.ordered= True
    order.order_id = orderId
    order.payment_id = val_id
    order.save()

    cart_items = Cart.objects.filter(user = request.user , purchased = False)
    for item in cart_items:
        item.purchased = True
        item.save()
    return HttpResponseRedirect(reverse("App_Shop:home"))





@login_required
def checkout(request):
    saved_address = BillingAddress.objects.get_or_create(user = request.user )[0]
    form = BillingForm(instance=saved_address)

    if request.method == "POST" or request.method == "post":
        form = BillingForm(request.POST, instance=saved_address)

        if form.is_valid():
            form.save()
            # form = BillingForm(instance=saved_address)
            messages.success(request,f"Shipping Address saved successfully!")
    
    order_qs = Order.objects.filter(user = request.user , ordered=False)
    print(order_qs) 
    order_items = order_qs[0].orderitems.all()
    print(order_items)
    order_total = order_qs[0].get_total()
    print(order_total)

    return render(request,'App_Payment/checkout.html',context={'form':form,'order_items':order_items,'order_total':order_total,'saved_address':saved_address})




@login_required
def order_view(request):
    try:
        orders = Order.objects.filter(user = request.user, ordered=True)
        context ={'orders':orders}
    
    except:
        messages.warning(request,f"You don't have any active order!")
        return redirect("App_Shop:home")

    return render(request,'App_Payment/order.html',context)