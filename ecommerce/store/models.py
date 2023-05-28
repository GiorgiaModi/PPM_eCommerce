from django.db import models
from django.contrib.auth.models import User


class CustomerModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)   #an user can only have a customer and a customer canonly have a user
    name = models.CharField(max_length=50, null=True)
    surname = models.CharField(max_length=50, null=True)
    email = models.EmailField(max_length=50, null=True)

    def __str__(self):
        return self.name


class ProductModel(models.Model):
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField()
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):   #senza questa funzione se ci fosse un prodotto senza immagine darebbe errore a tutta la pagina
        try:
            url = self.image.url
        except:
            url = ''
        return url


class OrderModel(models.Model):
    customer = models.ForeignKey(CustomerModel, on_delete=models.SET_NULL, blank=True, null=True)
    date_order = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=True)
    transaction_id = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.id)


class OrderItemModel(models.Model):
    product = models.ForeignKey(ProductModel, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(OrderModel, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)


class CheckOutModel(models.Model):
    name = models.CharField(max_length=20, default='')
    #name = models.ForeignKey(CustomerModel, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(OrderModel, on_delete=models.SET_NULL, null=True, blank=True)
    surname = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    postalCode = models.CharField(max_length=10)

    def __str__(self):
        return self.name
