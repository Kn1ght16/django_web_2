from django.core.management.base import BaseCommand, CommandError
from django_web_2.django_web_2.catalog.models import Category, Product


class Command(BaseCommand):
    help = 'Populate database with sample data'

    def handle(self, *args, **options):
        Category.objects.all().delete()
        Product.objects.all().delete()
