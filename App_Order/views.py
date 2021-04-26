from django.shortcuts import render,redirect,get_object_or_404


#Authentications
from django.contrib.auth.decorators import login_required

#Model
from .models import Cart, Order
from App_Shop.models import Product

#Messages
from django.contrib import messages

@login_required
def add_to_card(request,pk):
    item = get_object_or_404(Product,pk=pk)
    print("Item : ",item)
    order_item = Cart.objects.get_or_create(item = item, user= request.user, purchased=False)
    print("Order Item object : ",order_item)
    print("Order Item object[0] : ",order_item[0])
    order_qs = Order.objects.filter(user = request.user , ordered = False)
    print('Order qs : ',order_qs)
    

    if order_qs.exists():
        order = order_qs[0]
        print("If order exists : ",order)

        if order.orderitems.filter(item = item).exists():
            order_item[0].quantity += 1
            order_item[0].save()
            messages.info(request,"This item quantity was updated!")
            return redirect('App_Shop:home')
        else:
            order.orderitems.add(order_item[0])
            messages.info(request, "This item was added to your cart!")
            return redirect('App_Shop:home')
    else:
        order = Order(user = request.user)
        order.save()
        order.orderitems.add(order_item[0])
        messages.info(request,"This item was added to your cart!")
        return redirect('App_Shop:home')


@login_required
def cart_view(request):
    carts = Cart.objects.filter(user = request.user ,purchased=False)
    order = Order.objects.filter(user = request.user, ordered=False)

    if carts.exists() and order.exists():
        order = order[0]
        return render(request, 'App_Order/cart.html',context={'carts':carts,'order':order})
    
    else:
        messages.warning(request,"You don't have any item in your cart!")
        return redirect('App_Shop:home')


@login_required
def remove_from_cart(request,pk):
    item = get_object_or_404(Product,pk = pk)
    order_qs = Order.objects.filter(user = request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]

        if order.orderitems.filter(item = item).exists():
            order_item = Cart.objects.filter(item = item, user = request.user, purchased=False)[0]
            order.orderitems.remove(order_item)
            order_item.delete()
            messages.warning(request,"This item was removed from your cart!")
            return redirect("App_Order:cart")
        
        else:
            messages.info(request,"This item was not in your cart!")
    
    else:
        messages.info(request,"You don't have any active order.")
        return redirect('App_Shop:home')



@login_required
def increase_cart(request,pk):
    item = get_object_or_404(Product, pk = pk)
    order_qs = Order.objects.filter(user = request.user, ordered = False)

    if order_qs.exists():
        order = order_qs[0]

        if order.orderitems.filter(item = item).exists():
            order_item = Cart.objects.filter(item = item , user = request.user, purchased=False)[0]

            if order_item.quantity >= 1:
                order_item.quantity +=1
                order_item.save()
                messages.info(request,f"{item.name} quantity was updated!")
                return redirect("App_Order:cart")
            
        
        else:
            messages.info(request,f"{item.name} was not in your cart!")
            return redirect("App_Shop:home")

    else:
        messages.info(request,"You don't have any active order!")
        return redirect('App_Shop:home')



@login_required
def decrease_cart(request, pk):
    item = get_object_or_404(Product, pk = pk)
    order_qs = Order.objects.filter(user = request.user , ordered=False)

    if order_qs.exists():
        order = order_qs[0]

        if order.orderitems.filter(item = item ).exists():
            order_item = Cart.objects.filter(item = item, user = request.user, purchased=False)[0]
            
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
                messages.info(request,f"{item.name} quantity was updated!")
                return redirect("App_Order:cart")
            else:
                order.orderitems.remove(order_item)
                order_item.delete()
                messages.warning(request,"{item.name} was removed from your cart!")
                return redirect("App_Order:cart")
        else:
            messages.info(request,f"{item.name} was not in your cart!")
            return redirect("App_Shop:home")
    
    else:
        messages.info(request,"You don't have any active order!")
        return redirect('App_Shop:home')





    

