from django.shortcuts import render

# Create your views here.

def store (request):

    items_list = ['Elemento 1', 'Elemento 2', 'Elemento 3', 'Elemento 4', 'Elemento 5']
    return render(request, 'store/store.html',  {'items_list': items_list})

def cart (request):
    context ={}
    items_list = ['Elemento 1', 'Elemento 2', 'Elemento 3', 'Elemento 4', 'Elemento 5']
    return render(request, 'store/cart.html', {'items_list': items_list})

def checkout (request):
    context ={}
    items_list = ['Elemento 1', 'Elemento 2', 'Elemento 3', 'Elemento 4', 'Elemento 5']
    return render(request, 'store/checkout.html', {'items_list': items_list})
