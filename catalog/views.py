from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.forms import formset_factory
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.decorators.cache import cache_page

from .models import Product, Record, Version, Category
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView, View
from django.http import HttpResponse
from .forms import ProductForm, VersionFormSet, VersionForm
import redis


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_list = cache.get('category_list')
        if not category_list:
            category_list = list(Category.objects.values())
            cache.set('category_list', category_list)
        context['products'] = Product.objects.all()
        context['title'] = 'Главная страница'
        return context


class ContactView(TemplateView):
    template_name = 'contacts.html'
    extra_context = {
        'title': 'Контакты'
    }


class ProductListView(ListView):
    template_name = 'product_list.html'
    model = Product
    extra_context = {
        'object_list': Product.objects.all(),
        'title': 'Все продукты'  # дополнение к статической информации
    }


@login_required
def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.author = request.user  # Привязка продукта к авторизованному пользователю
            product.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'product_create.html', {'form': form})


@login_required
def update_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    VersionFormSet = formset_factory(VersionForm, extra=1)

    if request.method == 'POST':
        if product.author != request.user:
            return HttpResponse('Вы не являетесь владельцем продукта')

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


@login_required
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        if product.author != request.user:
            return HttpResponse('Вы не являетесь владельцем продукта')

        product.delete()
        return redirect('product_list')
    return render(request, 'product_confirm_delete.html', {'product': product})


def product_list(request):
    products = Product.objects.all()
    for product in products:
        product.active_version = Version.product.filter(product=product, is_current_version=True).first()
    return render(request, 'product_list.html', {'products': products})


@cache_page(60)
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


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.name
        if self.object.author == self.request.user:
            context['edit_url'] = reverse('product_update', kwargs={'pk': self.object.pk})
        return context


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
