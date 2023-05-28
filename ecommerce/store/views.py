from django.shortcuts import render
from .forms import CheckOutForm
from django.http import HttpResponseRedirect

# Create your views here.

def store (request):

    items_list = ['Elemento 1', 'Elemento 2', 'Elemento 3', 'Elemento 4', 'Elemento 5']
    return render(request, 'store/store.html',  {'items_list': items_list})

def cart (request):
    context ={}
    items_list = ['Elemento 1', 'Elemento 2', 'Elemento 3', 'Elemento 4', 'Elemento 5']
    return render(request, 'store/cart.html', {'items_list': items_list})


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
        form = CheckOutForm
        if 'submitted' in request.GET: #user submitted the form
            submitted = True

    form = CheckOutForm
    return render(request, 'store/checkout.html', {'form': form, 'submitted': submitted})
