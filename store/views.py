from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings

from store.utils import create_order
from .models import Brand, Order, Shoe, Cart, CartItem
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.views.decorators.cache import cache_page
from .payment import PaystackPayment


# Create your views here.

def homepage(request):
    shoes = Shoe.objects.only("id", "name", "price", "featured_image")[:8]
    context = {'shoes': shoes}

    return render(request, 'store/homepage/index.html', context)


def contact_page(request):
    return render(request, 'store/contact/contact.html')


# @cache_page(900)


def product_list(request):
    shoes = Shoe.objects.only(
        "id", "name", "price", "featured_image", "brand_id").select_related('brand')

    # Get filter and sorting parameters
    brand_id = request.GET.get('brand')
    sort_by = request.GET.get('sort_by')

    # Filter by brand if selected
    if brand_id and brand_id != 'all':
        shoes = shoes.filter(brand_id=brand_id)

    # Sorting options
    if sort_by == "name_asc":
        shoes = shoes.order_by("name")
    elif sort_by == "name_desc":
        shoes = shoes.order_by("-name")
    elif sort_by == "price_asc":
        shoes = shoes.order_by("price")
    elif sort_by == "price_desc":
        shoes = shoes.order_by("-price")

    # Paginate results
    paginator = Paginator(shoes, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'shoes': page_obj,
        'selected_brand': brand_id,
        'sort_by': sort_by,
        'brands': Brand.objects.prefetch_related('shoes'),
    }

    return render(request, 'store/products/products.html', context)


def product_detail(request, pk):
    shoe = get_object_or_404(Shoe, id=pk)
    featured_products = Shoe.objects.filter(brand_id=pk)[:3]
    context = {'shoe': shoe, "featured_products": featured_products}
    return render(request, 'store/product/product.html', context)


def cart_count(request):
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            total_items = cart.total_items()
        except Cart.DoesNotExist:
            total_items = 0
    else:
        total_items = 0

    return HttpResponse(total_items)


def add_to_cart(request, product_id):
    if request.user.is_authenticated:
        product = get_object_or_404(Shoe, id=product_id)
        cart, created = Cart.objects.get_or_create(
            user=request.user)

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart, product=product)
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        if request.headers.get('HX-Request'):
            return redirect('view_cart')
    else:
        return HttpResponse({"You must be logged in to add Item "})


def view_cart(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(
            user=request.user).first()

        context = {'cart': cart, }
        return render(request, 'partials/cart_items.html', context)
    else:
        return HttpResponse({"You must be logged in to view your cart "})


@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    cart_item.delete()
    if request.headers.get('HX-Request'):
        return redirect('view_cart')
    else:

        return redirect('view_cart')


@login_required
def update_cart_item(request, cart_item_id, action):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)

    if action == 'increase':
        cart_item.quantity += 1
    elif action == 'decrease' and cart_item.quantity >= 1:
        cart_item.quantity -= 1

    cart_item.save()

    if action == 'decrease' and cart_item.quantity < 1:
        cart_item.delete()
    return redirect('view_cart')


@login_required
def add_order(request):

    user = request.user
    order = create_order(user)
    if order:
        messages.success(request, "Order placed successfully!")
        return redirect("order_detail", pk=order.id)
    messages.error(request, "Failed to place order.")
    return redirect("cart_view")


@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "store/orders/order_list.html", {"orders": orders})


@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, id=pk)
    context = {'order': order}
    return render(request, "store/orders/order_detail.html", context)


@login_required
def checkout_view(request, order_id):
    try:
        order = Order.objects.get(id=order_id, user=request.user)
        # Generate new payment reference for each checkout attempt
        payment_reference = order.generate_payment_reference()

        context = {
            'order': order,
            'paystack_public_key': settings.PAYSTACK_PUBLIC_KEY,
            'payment_reference': payment_reference
        }
        return render(request, 'store/orders/checkout.html', context)
    except Order.DoesNotExist:
        messages.error(request, 'Order not found')
        return redirect('orders')


@login_required
def initialize_payment(request, order_id):
    try:
        order = Order.objects.get(id=order_id, user=request.user)
        payment = PaystackPayment.initialize_payment(order)

        if payment['status']:
            order.save_payment_reference(payment['reference'])
            return redirect(payment['payment_url'])

        return JsonResponse({
            'status': False,
            'message': payment['message']
        })
    except Order.DoesNotExist:
        return JsonResponse({
            'status': False,
            'message': 'Order not found'
        })


@login_required
def verify_payment(request, reference):
    try:
        order = Order.objects.get(payment_reference=reference)
        payment = PaystackPayment.verify_payment(reference)

        if payment['status']:
            if payment['payment_status'] == 'success':
                order.verify_payment()
                messages.success(request, 'Payment successful!')
                return redirect('order_detail', pk=order.id)
            else:
                order.status = 'failed'
                order.save()
                messages.error(request, 'Payment failed!')
                return redirect('checkout', order_id=order.id)

        messages.error(request, payment['message'])
        return redirect('checkout', order_id=order.id)

    except Order.DoesNotExist:
        messages.error(request, 'Order not found')
        return redirect('checkout')
