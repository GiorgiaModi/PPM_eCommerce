import json
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST

from .forms import CheckOutForm
from .models import *


# Create your views here.


def store(request):
    items_list = ProductModel.objects.all()
    context = {'items_list': items_list}
    return render(request, 'store/store.html',  context)


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customermodel
        order, created = OrderModel.objects.get_or_create(customer=customer, complete=False)
        items_list = order.orderitemmodel_set.all()   #rende tutti gli item di quell'ordine
    else:
        items_list = []
        order = {'calculate_cart_total': 0, 'calculate_checkout': 0}

    context = {'items_list': items_list, 'order': order}

    return render(request, 'store/cart.html', context)


#def checkout (request):
    #context ={}
    #items_list = ['Elemento 1', 'Elemento 2', 'Elemento 3', 'Elemento 4', 'Elemento 5']
    #return render(request, 'store/checkout.html', {'items_list': items_list})


def checkout(request):
    submitted = False
    if request.method == "POST":
        form = CheckOutForm(request.POST)  #se l'utente compila il forma e clicca "Submit" verranno passati i dati a CheckOutForm
        if form.is_valid():
            form.save() #save to database
            return HttpResponseRedirect('/checkout?submitted=True')
    else:
        if 'submitted' in request.GET: #user submitted the form
            submitted = True
    form = CheckOutForm

    if request.user.is_authenticated:
        customer = request.user.customermodel
        order, created = OrderModel.objects.get_or_create(customer=customer, complete=False)
        items_list = order.orderitemmodel_set.all()   #rende tutti gli item di quell'ordine
    else:
        items_list = []
        order = {'calculate_cart_total': 0, 'calculate_checkout': 0, 'calculate_cart_items': 0}

    context = {'items_list': items_list, 'order': order, 'form': form, 'submitted': submitted}

    return render(request, 'store/checkout.html', context)


def update_item(request):
   if request.method == 'POST':
       data = json.loads(request.body)

       itemId = data['itemId']
       action = data['action']
       print('Action:', action)
       print('itemId:', itemId)

       customer = request.user.customermodel
       print('Customer:', customer)
       item = ProductModel.objects.get(id=itemId)
       print('Item:', item)
       #get order or create one
       order, created = OrderModel.objects.get_or_create(customer=customer, complete=False)
       print('Order:', order)
       print('Order CREATO:', created)
       orderItem, created = OrderItemModel.objects.get_or_create(order=order, product=item)
       #se questo orderItem gia esiste nell'ordine, non voglio crearne uno nuovo ma incrementare la quantità
       print('OrderItem:', orderItem)
       print('OrderItem CREATO:', created)
       print('OrderItemQuantityPRIMA:', orderItem.quantity)
       if action == 'add-cart':
           orderItem.quantity = (orderItem.quantity + 1)
       elif action == 'remove':
           orderItem.quantity = (orderItem.quantity - 1)
       print('OrderItemQuantityDOPO:', orderItem.quantity)
       orderItem.save()

       if orderItem.quantity <= 0:
           orderItem.delete()

       return JsonResponse('Item was added', safe=False)


"""
def add_to_cart(request, id):
    item = ProductModel.objects.get(id=id)
   
    order = OrderModel.objects.filter(customer=request.user.customermodel, complete=False)
    if order.exists():
        order = order[0]
    
        #check if the order item is in the order
        if order.items.filter(productmodel__id=item.id).exists():
            order_item = OrderItemModel.objects.filter(product=item, order=order)[0]
            order_item.quantity += 1
            order_item.save()
    else:
        order = OrderModel.objects.create(customer=request.user.customermodel, complete=False)
        order_item = OrderItemModel.objects.create(product=item, order=order, quantity=1)
    

    return redirect('store/store')

"""