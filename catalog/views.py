from django.shortcuts import render
from .models import Product


def home(request):
    product_list = Product.objects.all()
    context = {
        'object_list': product_list,
        'title': 'Каталог',
    }
    return render(request, 'home.html', context)


def contacts(request):
    context = {
        'title': 'Контакты',
    }
    return render(request, 'contacts.html', context)



