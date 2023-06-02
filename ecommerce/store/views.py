
import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import CheckOutForm
import datetime


# Create your views here.


def store(request):
    items_list = []
    cart_items = 0
    if request.user.is_authenticated:
        customer = CustomerModel.objects.get(user=request.user)
        order, created = OrderModel.objects.get_or_create(customer=customer, complete=False)
        items_list = order.orderitemmodel_set.all()   #rende tutti gli item di quell'ordine
        cart_items = order.calculate_cart_items
    """
    else:
        items_list = []
        order = {'calculate_cart_total': 0, 'calculate_checkout': 0}
        cart_items = order['calculate_cart_items']
"""
    items_list = ProductModel.objects.all()
    context = {'items_list': items_list, 'cart_items': cart_items}
    return render(request, 'store/store.html',  context)


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customermodel
        order, created = OrderModel.objects.get_or_create(customer=customer, complete=False)
        items_list = order.orderitemmodel_set.all()   #rende tutti gli item di quell'ordine
        cart_items = order.calculate_cart_items
    else:
        items_list = []
        order = {'calculate_cart_total': 0, 'calculate_checkout': 0}
        cart_items = order['calculate_cart_items']

    context = {'items_list': items_list, 'order': order, 'cart_items': cart_items}

    return render(request, 'store/cart.html', context)

def checkout(request):
    model = CheckOutModel
    template_name = 'store/checkout.html'
    form_class = CheckOutForm
    submitted = False

    if request.method == "POST":
        items_list = []
        order = None
        cart_items = 0
        form = CheckOutForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            order = None
            if request.user.is_authenticated:
                customer = request.user.customermodel
                order, created = OrderModel.objects.get_or_create(customer=customer, complete=False)
                order.transaction_id = datetime.datetime.now().timestamp()
                order.complete = True
                order.date_order = datetime.datetime.now()
                order.save()
            post.order = order  # Assegna l'ordine corrente all'istanza del form
            post.save()
            print('form saved')
            return HttpResponseRedirect('/checkout?submitted=True')
    else:
        form = CheckOutForm()
        if 'submitted' in request.GET:
            submitted = True

        if request.user.is_authenticated:
            customer = request.user.customermodel
            order, created = OrderModel.objects.get_or_create(customer=customer, complete=False)
            items_list = order.orderitemmodel_set.all()
            cart_items = order.calculate_cart_items()
        else:
            items_list = []
            order = {'calculate_cart_total': 0, 'calculate_checkout': 0, 'calculate_cart_items': 0}
            cart_items = order['calculate_cart_items']

    context = {'items_list': items_list, 'order': order, 'form': form, 'submitted': submitted, 'cart_items': cart_items}

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
       if action == 'add':
           orderItem.quantity = (orderItem.quantity + 1)
       elif action == 'remove':
           orderItem.quantity = (orderItem.quantity - 1)
       print('OrderItemQuantityDOPO:', orderItem.quantity)
       orderItem.date_added = datetime.datetime.now()
       orderItem.save()

       if orderItem.quantity <= 0:
           orderItem.delete()

       return JsonResponse('Item was added', safe=False)


def search(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        items = ProductModel.objects.filter(name__contains=searched)
        return render(request, 'store/search.html', {'searched': searched, 'items': items})
    else:
        return render(request, 'store/search.html', {})


def detail(request, id):
    product = get_object_or_404(ProductModel, pk=id)

    return render(request, 'store/detail.html', {
        'product': product,
    })


@login_required
def likeProduct(request, id):
    username = request.user.username
    productId = id

    product = ProductModel.objects.get(pk=id)
    like_filter = LikedProducts.objects.filter(productId=productId, username=username).first()

    if not like_filter:
        like = LikedProducts.objects.create(productId=productId, username=username)
        #like = LikedProducts.objects.filter(productId=productId, username=username)
        like.save()
        product.numberOfLikes = product.numberOfLikes + 1
        product.save()
        return redirect('/detail/' + str(productId) + '/')
    else:
        like_filter.delete()
        product.numberOfLikes = product.numberOfLikes - 1
        product.save()
        return redirect('/detail/' + str(productId) + '/')


@login_required
def likedProducts(request):
    username = request.user.username
    products = LikedProducts.objects.filter(username=username)
    likedProd = ProductModel.objects.filter(id__in=products.values_list('productId', flat=True))

    return render(request, 'store/likedProducts.html', {
        'likedProducts': likedProd,
    })
