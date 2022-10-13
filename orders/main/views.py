from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.core.paginator import Paginator

from .models import Order


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


def delete(request, order_id):
    order = Order.objects.get(pk=order_id)
    order.delete()
    return redirect('home')


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
