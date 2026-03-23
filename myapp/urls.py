from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),          # Home page is the store
    path('signup/', views.sign_up, name='signup'), # Signup is at /signup/
    path('login/', views.log_in, name='login'),    # Login is at /login/
    path('logout/', views.log_out, name='logout'),
    path('cart/', views.cart_view, name='cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('place-order/', views.place_order, name='place_order'),
    path('order-success/', views.order_success, name='order_success'),
]