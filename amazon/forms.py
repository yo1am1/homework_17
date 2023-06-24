from django.forms import ModelForm

from amazon.models import Product


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ["title", "description", "price", "certificate"]
