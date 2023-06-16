from django.db import models
from django.urls import reverse
from django.core.exceptions import ValidationError

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

    def clean(self):
        prohibited_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']
        for word in prohibited_words:
            if word in self.name.lower() or word in self.description.lower():
                raise ValidationError(
                    f"Запрещенное слово '{word}' не может быть использовано в названии или описании продукта.")


class Version(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    version_number = models.CharField(max_length=50, verbose_name='Номер версии')
    version_name = models.CharField(max_length=150, verbose_name='Название версии')
    is_current_version = models.BooleanField(default=False, verbose_name='Текущая версия')

    def __str__(self):
        return f'Версия {self.version_number} ({self.product.name})'

    class Meta:
        verbose_name = 'версия'
        verbose_name_plural = 'версии'
        ordering = ('-is_current_version', 'version_number')


class Record(models.Model):
    record_title = models.CharField(max_length=150, verbose_name='Заголовок')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    content = models.TextField(max_length=15000, verbose_name='Содержимое')
    preview = models.ImageField(upload_to='image/', verbose_name='Изображение', null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True, verbose_name='Дата создания')
    sign_of_publication = models.BooleanField(default=True, verbose_name='Признак публикации')
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.record_title

    def get_absolute_url(self):
        return reverse('record_detail', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'запись'
        verbose_name_plural = 'записи'
        ordering = ('record_title', 'slug', 'created_at', 'sign_of_publication')

    def increase_views(self):
        self.views += 1
        self.save()
