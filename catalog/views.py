from django.forms import formset_factory
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy

from .models import Product, Record, Version
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView, View
from django.http import HttpResponse
from .forms import ProductForm, VersionFormSet, VersionForm


class IndexView(TemplateView):
    template_name = 'index.html'
    extra_context = {
        'title': 'Главная страница',
        'object_list': Product.objects.all()
    }


class ContactView(TemplateView):
    template_name = 'contacts.html'
    extra_context = {
        'title': 'Контакты'
    }


# def home(request):
#    product_list = Product.objects.all()
#    context = {
#        'object_list': product_list,
#        'title': 'Каталог',
#    }
#    return render(request, 'home.html', context)


# def contacts(request):
#    context = {
#        'title': 'Контакты',
#    }
#    return render(request, 'contacts.html', context)


class ProductListView(ListView):
    template_name = 'product_list.html'
    model = Product
    extra_context = {
        'object_list': Product.objects.all(),
        'title': 'Все продукты'  # дополнение к статической информации
    }


def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'product_create.html', {'form': form})


def update_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    VersionFormSet = formset_factory(VersionForm, extra=1)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        formset = VersionFormSet(request.POST, prefix='version')

        if form.is_valid() and formset.is_valid():
            form.save()
            for version_form in formset:
                version = version_form.save(commit=False)
                version.product = product
                version.save()

            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
        formset = VersionFormSet(prefix='version')

    return render(request, 'product_update.html', {'form': form, 'formset': formset})


def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    return render(request, 'product_confirm_delete.html', {'product': product})


def product_list(request):
    products = Product.objects.all()
    for product in products:
        product.active_version = Version.product.filter(product=product, is_current_version=True).first()
    return render(request, 'product_list.html', {'products': products})


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    formset = VersionFormSet(instance=product)
    if request.method == 'POST':
        formset = VersionFormSet(request.POST, instance=product)
        if formset.is_valid():
            formset.save()
            return redirect('product_detail', pk=pk)
    return render(request, 'product_detail.html', {'product': product, 'formset': formset})


class RecordListView(ListView):  # выведение контекста записей из модели по ключу object_list
    model = Record
    template_name = 'record_detail.html'
    context_object_name = 'records'
    extra_context = {
        'title': 'Все записи',  # дополнение к статической информации
    }

    def get_queryset(self):  # выводит только активные записи
        queryset = super().get_queryset()
        queryset = queryset.filter(sign_of_publication=True)
        return queryset


class RecordDetailView(DetailView):
    model = Record
    template_name = 'product_detail.html'
    context_object_name = 'object'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = self.get_object()
        return context_data

    def get_success_url(self):
        return reverse_lazy('record_detail', kwargs={'slug': self.object.slug})


class RecordCreateView(CreateView):
    model = Record
    fields = ('record_title', 'slug', 'content', 'preview')
    success_url = reversed('records_list')


class RecordUpdateView(UpdateView):
    model = Record
    fields = ('record_title', 'slug', 'content', 'preview')


class RecordDeleteView(DeleteView):
    model = Record
    success_url = reversed('records_list')


class ProductDetailView(DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = self.get_object()
        return context_data


class ProductItemView(View):
    def get(self, request, pk):

        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return HttpResponse('Товар не найден')

        # Вывод информации о товаре
        context = {
            'product': product
        }
        return render(request, 'product_item.html', context)
