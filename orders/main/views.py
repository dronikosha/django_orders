from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from .models import Order


def owner_check(func):
    def wrapper(request, order_id):
        order = Order.objects.get(pk=order_id)
        if order.owner == request.user:
            return func(request, order_id)
        else:
            return redirect('home')
    return wrapper


def check_exists(func):
    def wrapper(request, order_id):
        try:
            Order.objects.get(pk=order_id)
        except Order.DoesNotExist:
            return redirect('home')
        return func(request, order_id)
    return wrapper


def home(request):
    orders = Order.objects.all().reverse()
    paginator = Paginator(orders, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'main/home.html', {'page_obj': page_obj})


def search(request):
    if request.method == 'GET':
        if request.GET['search'] and request.GET['search'] != '':
            search = request.GET['search']
            orders = (Order.objects.filter(title__contains=search) |
                      Order.objects.filter(text__contains=search)).reverse()
            paginator = Paginator(orders, 4)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            return render(request, 'main/home.html', {'search': search, 'page_obj': page_obj})
        else:
            return redirect('home')
    else:
        return redirect('home')


@login_required
def create(request):
    if request.method == 'POST':
        if request.POST['title'] and request.POST['text']:
            order = Order()
            order.title = request.POST['title']
            order.text = request.POST['text']
            order.owner = request.user
            order.save()
            return redirect('home')
        else:
            return render(request, 'main/create.html', {'error': 'All fields are required.'})
    else:
        return render(request, 'main/create.html')


def order(request, order_id):
    order = Order.objects.get(pk=order_id)
    return render(request, 'main/order.html', {'order': order})


@check_exists
@login_required
@owner_check
def delete(request, order_id):
    order = Order.objects.get(pk=order_id)
    order.delete()
    return redirect('home')


@check_exists
@login_required
@owner_check
def update(request, order_id):
    order = Order.objects.get(pk=order_id)
    if request.method == 'POST':
        print(request.POST.get('title'))
        if request.POST['title'] and request.POST['text']:
            order.title = request.POST['title']
            order.text = request.POST['text']
            order.save()
            return redirect('home')
        else:
            return render(request, 'main/update.html', {'order': order, 'error': 'All fields are required.'})
    else:
        return render(request, 'main/update.html', {'order': order})


@login_required
def profile(request, username):
    profile_user = User.objects.get(username=username)
    orders = Order.objects.select_related(
        'owner').filter(owner=profile_user).reverse()
    paginator = Paginator(orders, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if request.method == 'GET' and request.GET.get('token'):
        token = Token.objects.get_or_create(user=request.user)
        print(token)
        return render(request, 'main/profile.html', {'profile_user': profile_user, 'page_obj': page_obj, 'token': token})
    else:
        return render(request, 'main/profile.html', {'profile_user': profile_user, 'page_obj': page_obj})
