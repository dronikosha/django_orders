from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .models import Order


def home(request):
    orders = Order.objects.all().reverse()
    return render(request, 'main/home.html', {'orders': orders})


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
