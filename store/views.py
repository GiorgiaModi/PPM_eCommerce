from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.http import JsonResponse
import json
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView
from .models import *
from .forms import CheckOutForm, ReviewForm
import datetime



def store(request):
    items_list = []
    cart_items = 0
    categories = CategoryModel.objects.all()
    if request.user.is_authenticated:
        customer = CustomerModel.objects.get(user=request.user)
        order, created = OrderModel.objects.get_or_create(customer=customer, complete=False)
        cart_items = order.calculate_cart_items

    items_list = ProductModel.objects.all().order_by('name')

    context = {'items_list': items_list, 'cart_items': cart_items, 'categories': categories}
    return render(request, 'store/store.html',  context)


def cart(request):
    customer = request.user.customermodel
    order, created = OrderModel.objects.get_or_create(customer=customer, complete=False)
    items_list = order.orderitemmodel_set.all()   #rende tutti gli item di quell'ordine
    cart_items = order.calculate_cart_items

    context = {'items_list': items_list, 'order': order, 'cart_items': cart_items}
    return render(request, 'store/cart.html', context)


def checkout(request):
    submitted = False

    if request.method == "POST":
        items_list = []
        order = None
        cart_items = 0
        form = CheckOutForm(request.POST)
        if form.is_valid():
            customer = request.user.customermodel
            order = OrderModel.objects.get(customer=customer, complete=False)
            order.transaction_id = datetime.datetime.now().timestamp()
            order.complete = True
            order.date_order = datetime.datetime.now()
            order.save() #FIXME: forse è questo che fa doppio ordine
            form.instance.order = order  # Assegna l'ordine corrente all'istanza del form
            form.save()
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
            order = None
            items_list = []
            cart_items = 0

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


def category(request, id):
    category = get_object_or_404(CategoryModel, pk=id)
    items = ProductModel.objects.filter(category=category)
    cart_items = 0
    if request.user.is_authenticated:
        customer = request.user.customermodel
        order, created = OrderModel.objects.get_or_create(customer=customer, complete=False)
        cart_items = order.calculate_cart_items
    else:
        order = None
        cart_items = 0

    return render(request, 'store/category_page.html', {
        'category': category,
        'items': items,
        'cart_items': cart_items,
    })


def search(request):
    cart_items = 0
    if request.user.is_authenticated:
        customer = request.user.customermodel
        order, created = OrderModel.objects.get_or_create(customer=customer, complete=False)
        cart_items = order.calculate_cart_items
    else:
        order = None
        cart_items = 0

    if request.method == 'POST':
        searched = request.POST['searched']
        items = ProductModel.objects.filter(name__contains=searched)
        return render(request, 'store/search.html', {'searched': searched, 'items': items, 'cart_items': cart_items})
    else:
        return render(request, 'store/search.html', {'cart_items': cart_items})


def detail(request, id):
    product = get_object_or_404(ProductModel, pk=id)
    liked_object = LikedProducts.objects.filter(productId=id, username=request.user.username).first()
    cart_items = 0
    if request.user.is_authenticated:
        customer = request.user.customermodel
        order, created = OrderModel.objects.get_or_create(customer=customer, complete=False)
        cart_items = order.calculate_cart_items
    else:
        cart_items = 0

    return render(request, 'store/detail.html', {
        'product': product,
        'cart_items': cart_items,
        'liked_object': liked_object,
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
    if request.user.is_authenticated:
        customer = request.user.customermodel
        order, created = OrderModel.objects.get_or_create(customer=customer, complete=False)
        cart_items = order.calculate_cart_items
    return render(request, 'store/likedProducts.html', {
        'likedProducts': likedProd,
        'cart_items': cart_items,
    })


def addReview(request, id):
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            customer = request.user.customermodel
            form.instance.customer = customer
            form.instance.date_added = datetime.datetime.now()
            product = ProductModel.objects.get(id=id)
            form.instance.product = product
            form.save()
            detail_url = reverse('detail', args=[id])
            return redirect(detail_url)
    else:
        form = ReviewForm()

    if request.user.is_authenticated:
        customer = request.user.customermodel
        order, created = OrderModel.objects.get_or_create(customer=customer, complete=False)
        cart_items = order.calculate_cart_items
    else:
        cart_items = 0
    context = {'form': form, 'cart_items': cart_items}
    return render(request, 'store/add_review.html', context)


def deleteReview(request, id):
    review = get_object_or_404(Review, id=id)
    product_id = review.product.id
    review.delete()
    detail_url = reverse('detail', args=[product_id])
    return redirect(detail_url)