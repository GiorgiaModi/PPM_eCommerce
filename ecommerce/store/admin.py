from django.contrib import admin
from .models import CustomerModel
from .models import ProductModel
from .models import OrderModel
from .models import OrderItemModel
from .models import CheckOutModel


admin.site.register(CustomerModel)
admin.site.register(ProductModel)
admin.site.register(OrderModel)
admin.site.register(OrderItemModel)
admin.site.register(CheckOutModel)

