from django.shortcuts import render, get_object_or_404, redirect
from .models import Shoe, Cart, CartItem
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.decorators.cache import cache_page


# Create your views here.

def homepage(request):
    shoes = Shoe.objects.only("id", "name", "price", "featured_image")[:8]
    context = {'shoes': shoes}

    return render(request, 'store/homepage/index.html', context)


def contact_page(request):
    return render(request, 'store/contact/contact.html')


@cache_page(900)
def product_list(request):
    shoes = Shoe.objects.only(
        "id", "name", "price", "featured_image", "brand_id").select_related('brand')

    # Get filter and sorting parameters
    brand_id = request.GET.get('brand')
    sort_by = request.GET.get('sort_by')

    # Filter by brand if selected
    if brand_id:
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
        'sort_by': sort_by
    }
    return render(request, 'store/products/products.html', context)


def product_detail(request, pk):
    shoe = get_object_or_404(Shoe, id=pk)
    context = {'shoe': shoe}
    return render(request, 'store/product/product.html', context)


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
