from django.urls import path
from . import views

urlpatterns = [
    # Login Page
    path('', views.login_user, name='login'),

    # Authentication
    path('login/', views.login_user, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_user, name='logout'),

    # Home
    path('home/', views.home, name='home'),

    # Products
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),

    # Wishlist
    path('wishlist/', views.wishlist, name='wishlist'),
    path('wishlist/add/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),

    # Cart
    path('cart/', views.cart, name='cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),

    # Checkout
    path('checkout/', views.checkout, name='checkout'),
    path('place-order/', views.place_order, name='place_order'),

    # Orders
    path('orders/', views.orders, name='orders'),
]