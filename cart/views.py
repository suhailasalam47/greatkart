from django.shortcuts import render, redirect
from store.models import Product, Variation
from .models import *
# Create your views here.

def _cart_id(request):
    cart_id = request.session.session_key
    if not cart_id:
        cart_id = request.session.create
    return cart_id


def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    product_variation = []
    if request.method == 'POST':
        for item in request.POST:
            key = item
            value = request.POST[key]
            try:
                variation = Variation.objects.get(
                    variation_category__iexact = key,
                    variation_value__iexact = value,
                    product = product
                )
                product_variation.append(variation)
            except:
                pass
    try:
        cart = Cart.objects.get(cart_id = _cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id = _cart_id(request)
        )
    cart.save()

    cart_item_exists = CartItem.objects.filter(
            product = product,
            cart = cart
        ).exists()
    if cart_item_exists:
        cart_item = CartItem.objects.filter(
            product = product,
            cart = cart
        )
        ex_var_list = []
        id = []
        for item in cart_item:
            existing_variation = item.variations.all()
            ex_var_list.append(list(existing_variation))
            id.append(item.id)
        print(ex_var_list)
        print(product_variation)

        if product_variation in ex_var_list:
            index = ex_var_list.index(product_variation)
            item_id = id[index]
            item = CartItem.objects.get(product=product, id=item_id)
            item.quantity +=1
            item.save()
        elif product_variation[::-1] in ex_var_list:
            index =  ex_var_list.index(product_variation[::-1])
            item_id = id[index]
            item = CartItem.objects.get(product=product, id=item_id)
            item.quantity +=1
            item.save()
        else:
            item = CartItem.objects.create(product=product, cart=cart, quantity=1)
            if len(product_variation)>0:
                item.variations.clear()
                item.variations.add(*product_variation)
            item.save()
    else:
        cart_item = CartItem.objects.create(
            product = product,
            cart = cart,
            quantity = 1
        )
        if len(product_variation)>0:
            cart_item.variations.clear()
            cart_item.variations.add(*product_variation)
        cart_item.save()
    return redirect('cart')


def remove_cart(request, product_id, cart_item_id):
    product = Product.objects.get(id=product_id)
    cart = Cart.objects.get(cart_id=_cart_id(request))
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
        if cart_item.quantity >1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')


def remove_cart_item(request, product_id, cart_item_id):
    product = Product.objects.get(id=product_id)
    cart = Cart.objects.get(cart_id=_cart_id(request))
    cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
    cart_item.delete()
    return redirect('cart')


def cart(request, quantity=0, total=0, cart_items=None):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active = True)
        for cart_item in cart_items:
            quantity += cart_item.quantity
            total += (cart_item.quantity * cart_item.product.price)
        tax = (2*total)/100
        grand_total = total + tax
    except:
        pass
    context = {
        'quantity' : quantity,
        'total' : total,
        'cart_items' : cart_items,
        'tax' : tax,
        'grand_total' : grand_total
    }
    return render(request, 'store/cart.html', context)