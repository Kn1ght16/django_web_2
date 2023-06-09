from django.db import models
from django.urls import reverse

NULLABLE = {'blank': True, 'null': True}


class Category(models.Model):
    objects = None
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name}'


class Product(models.Model):
    DoesNotExist = None
    objects = None
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='product_images/', **NULLABLE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"


class Record(models.Model):
    record_title = models.CharField(max_length=150, verbose_name='Заголовок')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    content = models.TextField(max_length=15000, verbose_name='Содержимое')
    preview = models.ImageField(upload_to='image/', verbose_name='Изображение', **NULLABLE)
    created_at = models.DateTimeField(auto_now=True, verbose_name='Дата создания')
    sign_of_publication = models.BooleanField(default=True, verbose_name='Признак публикации')

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.views = None

    def __str__(self):
        return f'{self.record_title}'

    def get_absolute_url(self):
        return reverse('record_detail', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'запись'
        verbose_name_plural = 'записи'
        ordering = ('record_title', 'slug', 'created_at', 'sign_of_publication')

    def increase_views(self):
        self.views += 1
        self.save()
