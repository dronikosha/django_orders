from django.shortcuts import render, redirect
from .forms import UserForm


def registration(request):
    form = UserForm()
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    return render(request, 'registration/registration.html', {'form': form})
