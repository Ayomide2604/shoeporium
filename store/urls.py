from django.urls import path
from . import views
urlpatterns = [
    path('', views.homepage, name='home'),
    path('contact_us/', views.contact_page, name='contact'),

    # Product
    path('products/', views.product_list, name='products'),
    path('product/<int:pk>/', views.product_detail, name='product'),


    # Cart
    path('cart-count/', views.cart_count, name='cart_count'),
    path('product/<int:product_id>/add-to-cart/',
         views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('remove-from-cart/<int:cart_item_id>/',
         views.remove_from_cart, name='remove_from_cart'),
    path('update-cart-item/<int:cart_item_id>/<str:action>/',
         views.update_cart_item, name='update_cart_item'),

    # Order
    path("checkout/", views.checkout, name="checkout"),
    path("orders/", views.order_list, name="order_list"),
    path("order/<str:pk>", views.order_detail, name="order_detail"),
]
