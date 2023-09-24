from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from user.models import Profile
from .forms import ProductForm
from .models import Category, Product, Favorite
from basket.forms import CartAddProductForm


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    favorites = Favorite.objects.all()
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    sort_by = request.GET.get('sort_by')
    if sort_by == 'price_low_to_high':
        products = products.order_by('price')
    elif sort_by == 'price_high_to_low':
        products = products.order_by('-price')
    elif sort_by == 'date_added_new_to_old':
        products = products.order_by('-created')
    elif sort_by == 'date_added_old_to_new':
        products = products.order_by('created')
    return render(request,
                  'shop/list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products,
                   'favorites': favorites})


def product_detail(request, id, slug):
    product = get_object_or_404(Product,
                                id=id,
                                slug=slug,
                                available=True)
    cart_product_form = CartAddProductForm()
    return render(request,
                  'shop/detail.html',
                  {'product': product,
                   'cart_product_form': cart_product_form
                   })


@login_required
def create_product(request):
    if request.method == 'GET':
        return render(request, 'shop/create_product.html', {'form': ProductForm()})
    else:
        try:
            form = ProductForm(request.POST)
            new_product = form.save(commit=False)
            new_product.user = request.user
            new_product.save()
            return redirect('list')
        except ValueError:
            return render(request, 'shop/create_product.html',
                          {'form': ProductForm(),
                           'error': 'Что-то пошло не так'})


@login_required()
def update_product(request, product_pk):
    product = get_object_or_404(Product, product_pk)
    form = ProductForm(instance=product)
    if request.method == "GET":
        return render(request, 'shop/update_product.html', {'product': product, 'form': form})
    else:
        try:
            form = ProductForm(request.POST, instance=product)
            form.save()
        except ValueError:
            return render(request, 'shop/update_product.html', {'form': form, 'error': 'Неверные данные!'})
        else:
            return redirect('list')


@login_required
def add_favorite(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.is_favorite = True
    product.save()
    return redirect('shop:product_list')

@login_required
def add_favorite(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, product=product)
    product.save()
    return redirect('shop:product_list')


@login_required
def remove_favorite(request, favorite_id):
    favorite = get_object_or_404(Favorite, id=favorite_id, user=request.user)
    favorite.delete()
    return redirect('shop:product_list')


@login_required
def favorite_list(request):
    favorites = Favorite.objects.filter(user=request.user)
    return render(request, 'shop/favorite_list.html', {'favorites': favorites})
