from django.core.management.base import BaseCommand
from django_web_2.catalog.models import Category, Product


class Command(BaseCommand):
    name = 'fill'

    def handle(self, *args, **options):
        Category.objects.all().delete()
        Product.objects.all().delete()

        category_list = [
            {"name": "Category 1", "description": "Description for category 1"},
            {"name": "Category 2", "description": "Description for category 2"},
            {"name": "Category 3", "description": "Description for category 3"}
        ]

        category_objects = []
        for category_item in category_list:
            category_objects.append(
                Category(**category_item)
            )

        Category.objects.bulk_create(category_objects)
