from django.contrib import admin
from .models import Product, Category


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category') # отображаемые поля
    list_filter = ('category',) # фильтрация по категории
    search_fields = ('name', 'description') # поиск по названию и описанию


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)