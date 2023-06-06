from django.contrib import admin
from .models import CustomerModel
from .models import ProductModel
from .models import OrderModel
from .models import OrderItemModel
from .models import CheckOutModel
from .models import LikedProducts
from .models import CategoryModel
from .models import Review


admin.site.register(CustomerModel)
admin.site.register(ProductModel)
admin.site.register(OrderModel)
admin.site.register(OrderItemModel)
admin.site.register(CheckOutModel)
admin.site.register(LikedProducts)
admin.site.register(CategoryModel)
admin.site.register(Review)