from django.shortcuts import render, redirect
from django.urls import reverse

from amazon.forms import ProductForm
from amazon.models import Product


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
    return render(request, "images_list.html", {"images": images_display})
