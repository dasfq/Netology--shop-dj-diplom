from django.shortcuts import render, redirect, HttpResponseRedirect
from .models import Article, Category, Item, CustomUser, Review, Cart, CartInfo, OrderInfo, Order
from django.core.paginator import Paginator
from django.contrib.auth import views as auth_views
from .forms import UserForm, ReviewForm
from django.shortcuts import reverse
import urllib
from django.contrib.auth import get_user_model
from datetime import datetime
from django.contrib.auth.decorators import login_required
from functools import reduce



def index(request):
    template_name = 'index.html'
    articles = Article.objects.order_by('-date_created')

    context = {
        'articles': articles,
    }
    return render(request, template_name, context)

def item_page(request, pk):
    template_name = 'item.html'
    item = Item.objects.get(id=pk)
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            stars = form.cleaned_data.get('stars')
            text = form.cleaned_data.get('text')
            user = request.user
            date = datetime.now()
            Review.objects.create(stars=stars, text=text, user=user, item=item, date=date)
            return redirect("item_page", item.id)
    else:
        form = ReviewForm()
    context = {
        "item": item,
        "form": form,
    }
    return render(request, template_name, context)


@login_required
def add_to_cart(request, pk):
    redirect_to = request.GET.get('next')
    if request.method == 'POST':
        user = request.user
        item = Item.objects.get(id=pk)
        cart, is_created = Cart.objects.get_or_create(user=user)
        cart_info, is_created = CartInfo.objects.get_or_create(cart=cart, item=item)
        if not is_created:
            cart_info.quantity += 1
            cart_info.save()
        return HttpResponseRedirect(redirect_to)


def cart(request):
    template_name = 'cart.html'
    user = request.user
    cart, is_created = Cart.objects.get_or_create(user=user)
    cart_info = CartInfo.objects.filter(cart=cart)
    total_qty = sum([x.quantity for x in cart_info])
    context = {
        'cart': cart_info,
        'total': total_qty,
    }
    return render(request, template_name, context)

def make_order(request):
    user = request.user
    cart = Cart.objects.get(user=user)
    items_list = cart.cartinfo_set.all()
    order = Order.objects.create(user=user)
    for item in items_list:
        order_info = OrderInfo.objects.create(order=order, item=item.item, quantity = item.quantity)
    cart.delete()
    return redirect('index')

def empty_section(request):
    template_name = 'empty_section.html'
    context = {}
    return render(request, template_name, context)

def category_view(request, pk):
    template_name = 'category.html'
    items_per_page = 3
    items = Item.objects.filter(category__id=pk)
    if len(items) == 0:
        return redirect('empty_section')
    p = Paginator(items, items_per_page)
    page_number = 1 if request.GET.get('page') == None else int(request.GET.get('page'))
    if p.page(page_number).has_next():
        next_page_url = reverse('category', args=[pk]) + '?' + urllib.parse.urlencode({'page': p.page(page_number).next_page_number()})
    else:
        next_page_url = None
    if p.page(page_number).has_previous():
        prev_page_url = reverse('category', args=[pk]) + '?' + urllib.parse.urlencode(
        {'page': p.page(page_number).previous_page_number()})
    else:
        prev_page_url = None
    context = {
        "items": p.page(page_number),
        "category": Category.objects.get(id=pk).name,
        'current_page': page_number,
        'prev_page_url': prev_page_url,
        'next_page_url': next_page_url,
    }
    return render(request, template_name, context)


def signup(request):
    User = get_user_model()
    if request.method == 'POST':
        form = UserForm(request.POST)
        form.Meta.model = User
        if form.is_valid():
            password = form.cleaned_data.get('password1')
            email = form.cleaned_data.get('email')
            User.objects.create_user(email,password)
    else:
        form = UserForm()
    context={
        'form': form,
    }
    return render(request, 'registration/signup.html', context)

