from django.contrib import admin
from .models import Product, Category, Wishlist, Cart
from .models import Product, Category, Wishlist, Cart, Order



admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Wishlist)
admin.site.register(Cart)
admin.site.register(Order)