from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product 

@login_required(login_url='/login/')
def index(request):
    products = Product.objects.all()
    # Getting cart count for the navbar icon badge
    cart_count = len(request.session.get('cart', []))
    return render(request, 'index.html', {'products': products, 'cart_count': cart_count})

def cart_view(request):
    # 1. Fetch product IDs from session
    cart_ids = request.session.get('cart', [])
    
    # 2. Fetch actual Product objects
    cart_items = Product.objects.filter(id__in=cart_ids)
    
    # 3. Calculate total
    total_price = sum(item.price for item in cart_items)
    
    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
    })

def add_to_cart(request, product_id):
    cart = request.session.get('cart', [])
    if int(product_id) not in cart:
        cart.append(int(product_id))
    
    request.session['cart'] = cart
    request.session.modified = True 
    
    # Redirect back to the index page so they can keep shopping!
    return redirect('index')

def remove_from_cart(request, product_id):
    cart = request.session.get('cart', [])
    if int(product_id) in cart:
        cart.remove(int(product_id))
    request.session['cart'] = cart
    return redirect('cart')

def sign_up(request):
    if request.method == 'POST':
        username = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmPassword')

        if password != confirm_password:
            messages.info(request, "Passwords do not match.")
            return redirect('signup') 

        if User.objects.filter(username=username).exists():
            messages.info(request, "User already exists.")
            return redirect('login')
            
        # 1. Create the user
        user = User.objects.create_user(username=username, password=password)
        user.save()

        # 2. AUTO-LOGIN: This is the magic step
        # We authenticate first to ensure the backend session is linked
        authenticated_user = authenticate(username=username, password=password)
        if authenticated_user is not None:
            auth_login(request, authenticated_user)
            messages.success(request, f"Welcome to TrendStore, {username}!")
            return redirect('/') # Go straight to shopping!
    
    return render(request, 'signup.html')

def log_in(request):
    if request.method == "POST":
        username = request.POST.get("email")
        password = request.POST.get("password")

        if not User.objects.filter(username=username).exists():
            messages.error(request, "Invalid email.")
            return redirect('signup')

        user = authenticate(username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            return redirect('/') # Redirects to index
        else:
            messages.error(request, "Invalid credentials.")
            return redirect('login')

    # MATCHED: Changed from 'log_in.html' to 'login.html'
    return render(request, 'login.html')

def place_order(request):
    # 1. Get the list of product IDs from the session
    cart_ids = request.session.get('cart', [])
    
    # 2. Fetch those specific products from the database
    cart_items = Product.objects.filter(id__in=cart_ids)
    
    # 3. Calculate total price
    total_price = sum(item.price for item in cart_items)
    cart_count = len(cart_ids)
    
    # 4. Render the order page with the data
    return render(request, 'placeorder.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'cart_count': cart_count
    })

def order_success(request):
    # Clear the session cart after successful 'payment'
    if 'cart' in request.session:
        del request.session['cart']
    
    return render(request, 'order_success.html')

def log_out(request):
    logout(request)
    return redirect('login')