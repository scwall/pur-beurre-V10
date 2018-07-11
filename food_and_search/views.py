from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.urls import reverse

from food_and_search.models import Categorie, Product


def index(request):
    return render(request, 'index.html')


@login_required(login_url='/login/')
def save_product(request):
    current_user = request.user
    user_products = Product.objects.filter(user_product__exact=current_user.id)
    paginator = Paginator(user_products, 6)
    page = request.GET.get('product')
    products_paginator = paginator.get_page(number=page)
    context = {'products': products_paginator}
    if request.method == 'POST':
        current_user = request.user
        id_product = int(request.POST['product_form'])
        product = Product.objects.get(id=id_product)
        product.user_product.remove(current_user)
        context['save_product'] = 'Produit supprimé '
        context['id_product'] = id_product

    return render(request, 'save_product.html', context)


def result(request):
    if request.method == 'GET':
        product_cleaned = request.GET.get('product')

        if product_cleaned is None:
            print('test')
            raise Http404('Aucun produit demandé')
        else:
            product = Product.objects.filter(name__icontains=product_cleaned)
            if product.exists():
                categories = Categorie.objects.filter(products__id=product[0].id)
                products = Product.objects.filter(categorie__in=categories).order_by('nutrition_grade')
                paginator = Paginator(products, 6)
                page = request.GET.get('product')
                products_paginator = paginator.get_page(number=page)
                context = {'products': products_paginator, 'original_product':product_cleaned}

            else:
                raise Http404(product_cleaned)
        return render(request, 'result_product.html', context)
    if request.method == 'POST':
        context = {}
        if request.user.is_authenticated:
            current_user = request.user
            id_product = int(request.POST.get('product_form'))
            print(id_product)
            product = Product.objects.get(id=id_product)
            product.user_product.add(current_user)
            context['save_product'] = 'Produit sauvegardé'
            context['id_product'] = id_product
            print('post methode')
        else:
            return redirect('/login')

        return redirect(reverse('food_and_search:result')+ '?product={}'.format(request.POST['original_product']))


def detail_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, template_name='detail_product.html', context={'detail_product': product})


@login_required(login_url='/login/')
def user_account(request):
    return render(request, template_name='user_page.html')


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user_tmp = form.save()
            user_tmp.save()
            tmp_username = form.cleaned_data.get('username')
            tmp_password = form.cleaned_data.get('password')

            user = authenticate(username=tmp_username, password=tmp_password)
            login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})
