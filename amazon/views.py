from django.shortcuts import render, redirect
from django.urls import reverse

from amazon.forms import ProductForm, SignUpForm
from amazon.models import Product
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def add_image(request):
    form = ProductForm(request.POST, request.FILES)

    if request.method == "GET":
        form = ProductForm()
        return render(request, "images.html", {"form": form})

    if form.is_valid():
        form.save()
        return redirect(reverse(images))
    return render(request, "images.html", {"form": form})


def images(request):
    images_display = Product.objects.all()
    return render(request, "images_list.html", {"images": images_display, "user": request.user})
