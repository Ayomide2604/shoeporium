from .models import Cart, Brand


def cart_context(request):
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            total_items = cart.total_items()
        except Cart.DoesNotExist:
            total_items = 0
    else:
        total_items = 0

    return {'cart_items': total_items}


def brand_context(request):
    brands = Brand.objects.all()
    return {'brands': brands}
