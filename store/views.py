from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm

from .models import Product, Category, Wishlist, Cart, Order
from .forms import RegisterForm


# ---------------- HOME ----------------

def home(request):
    query = request.GET.get('q')
    category = request.GET.get('category')

    products = Product.objects.all()
    categories = Category.objects.all()

    if query:
        products = products.filter(name__icontains=query)

    if category:
        products = products.filter(category__id=category)

    return render(request, 'home.html', {
        'products': products,
        'categories': categories
    })


# ---------------- PRODUCT DETAILS ----------------

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html', {
        'product': product
    })


# ---------------- REGISTER ----------------

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')

    else:
        form = RegisterForm()

    return render(request, 'register.html', {
        'form': form
    })


# ---------------- LOGIN ----------------

def login_user(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            login(request, form.get_user())
            return redirect('home')

    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {
        'form': form
    })


# ---------------- LOGOUT ----------------

def logout_user(request):
    logout(request)
    return redirect('home')


# ---------------- WISHLIST ----------------

@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    Wishlist.objects.get_or_create(
        user=request.user,
        product=product
    )

    return redirect('wishlist')


@login_required
def wishlist(request):
    items = Wishlist.objects.filter(user=request.user)

    return render(request, 'wishlist.html', {
        'items': items
    })


# ---------------- CART ----------------

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    cart_items = Cart.objects.filter(
        user=request.user,
        product=product
    )

    if cart_items.exists():
        cart_item = cart_items.first()
        cart_item.quantity += 1
        cart_item.save()

        # Remove duplicate rows if they exist
        cart_items.exclude(id=cart_item.id).delete()
    else:
        Cart.objects.create(
            user=request.user,
            product=product,
            quantity=1
        )

    return redirect('cart')


@login_required
def cart(request):
    items = Cart.objects.filter(user=request.user)

    total = sum(
        item.product.price * item.quantity
        for item in items
    )

    return render(request, 'cart.html', {
        'items': items,
        'total': total
    })


# ---------------- CHECKOUT ----------------

@login_required
def checkout(request):
    items = Cart.objects.filter(user=request.user)

    total = sum(
        item.product.price * item.quantity
        for item in items
    )

    return render(request, 'checkout.html', {
        'items': items,
        'total': total
    })


# ---------------- PLACE ORDER ----------------

@login_required
def place_order(request):
    cart_items = Cart.objects.filter(user=request.user)

    for item in cart_items:
        Order.objects.create(
            user=request.user,
            product=item.product,
            quantity=item.quantity,
            total_price=item.product.price * item.quantity
        )

    cart_items.delete()

    return redirect('orders')


# ---------------- ORDER HISTORY ----------------

@login_required
def orders(request):
    orders = Order.objects.filter(user=request.user)

    return render(request, 'orders.html', {
        'orders': orders
    })