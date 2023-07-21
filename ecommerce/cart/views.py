from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect

from cart.cart import Cart
from store.models import Product
from decimal import Decimal


def cart_summary(request):
    cart = Cart(request)

    # Check if a coupon code is submitted
    if request.POST.get('action') == 'apply_coupon':
        coupon_code = request.POST.get('coupon_code')
        cart.apply_coupon(coupon_code)

    # Check if a coupon removal is requested
    if request.POST.get('action') == 'remove_coupon':
        cart.remove_coupon()

    return render(request, 'cart/cart-summary.html', {'cart': cart, 'title': 'Shopping cart'})

def cart_add(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_quantity = int(request.POST.get('product_quantity'))
        product = get_object_or_404(Product, id=product_id)
        cart.add(product=product, product_qty=product_quantity)
        cart_quantity = cart.__len__()
        response = JsonResponse({'qty': cart_quantity})
        return response


def cart_clear(request):
    del request.session['session_key']
    return redirect('cart:cart-summary')


def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        cart.delete(product=product_id)
        cart_quantity = cart.__len__()
        cart_total = cart.get_total()
        response = JsonResponse({'qty': cart_quantity, 'total': cart_total})
        return response

def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_quantity = int(request.POST.get('product_quantity'))
        cart.update(product=product_id, qty=product_quantity)
        cart_quantity = cart.__len__()
        cart_total = cart.get_total()
        response = JsonResponse({'qty': cart_quantity, 'total': cart_total})
        return response





