from django.shortcuts import render
from .models import Product, Record
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView, View
from django.http import HttpResponse


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
