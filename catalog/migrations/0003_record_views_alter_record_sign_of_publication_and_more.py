# Generated by Django 4.2.1 on 2023-06-11 02:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_record_alter_product_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='record',
            name='views',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='record',
            name='sign_of_publication',
            field=models.BooleanField(default=True, verbose_name='Признак публикации'),
        ),
        migrations.CreateModel(
            name='Version',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version_number', models.CharField(max_length=50, verbose_name='Номер версии')),
                ('version_name', models.CharField(max_length=150, verbose_name='Название версии')),
                ('is_current_version', models.BooleanField(default=False, verbose_name='Текущая версия')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.product')),
            ],
            options={
                'verbose_name': 'версия',
                'verbose_name_plural': 'версии',
                'ordering': ('-is_current_version', 'version_number'),
            },
        ),
    ]