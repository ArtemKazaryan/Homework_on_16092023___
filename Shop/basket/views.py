from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product
from .cart import Basket
from .forms import CartAddProductForm


@require_POST
def basket_add(request, product_id):
    basket = Basket(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        basket.add(product=product,
                   quantity=cd['quantity'],
                   update_quantity=cd['update'])
    return redirect('basket:basket_detail')


def cart_remove(request, product_id):
    basket = Basket()
    product = get_object_or_404(Product, id=product_id)
    basket.remove(product)
    return redirect('basket:basket')


def basket_detail(request):
    basket = request
    return render(request, 'basket/detail.html', {'basket': basket})
