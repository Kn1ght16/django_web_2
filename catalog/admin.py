from django.contrib import admin
from .models import Product, Category, Record


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category')  # отображаемые поля
    list_filter = ('category',)  # фильтрация по категории
    search_fields = ('name', 'description')  # поиск по названию и описанию


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_filter = ('name',)


@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'record_title',)
    list_filter = ('record_title',)
    search_fields = ('record_title',)

# admin.site.register(Product, ProductAdmin)
# admin.site.register(Category, CategoryAdmin)
# admin.site.register(Record)
