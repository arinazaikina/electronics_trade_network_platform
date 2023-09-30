# Generated by Django 4.2 on 2023-09-26 18:30

import app_shop.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_supplier', models.CharField(choices=[('factory', 'Завод'), ('retail', 'Розничная сеть'), ('entrepreneur', 'Индивидуальный предприниматель')], max_length=12, verbose_name='Тип звена')),
                ('name', models.CharField(max_length=100, validators=[app_shop.validators.validate_not_blank], verbose_name='Название')),
                ('email', models.EmailField(max_length=254, verbose_name='Электронная почта')),
                ('country', models.CharField(max_length=100, validators=[app_shop.validators.validate_not_blank], verbose_name='Страна')),
                ('city', models.CharField(max_length=100, validators=[app_shop.validators.validate_not_blank], verbose_name='Город')),
                ('street', models.CharField(max_length=100, validators=[app_shop.validators.validate_not_blank], verbose_name='Улица')),
                ('house_number', models.CharField(max_length=10, validators=[app_shop.validators.validate_not_blank], verbose_name='Номер дома')),
                ('debt', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Задолженность перед поставщиком')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Время создания')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children', to='app_shop.supplier', verbose_name='Поставщик')),
            ],
            options={
                'verbose_name': 'Звено сети',
                'verbose_name_plural': 'Звенья сети',
                'db_table': 'suppliers',
                'unique_together': {('country', 'city', 'name', 'email')},
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, validators=[app_shop.validators.validate_not_blank], verbose_name='Название')),
                ('model', models.CharField(max_length=100, validators=[app_shop.validators.validate_not_blank], verbose_name='Модель')),
                ('release_date', models.DateField(verbose_name='Дата выхода на рынок')),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_shop.supplier', verbose_name='Поставщик')),
            ],
            options={
                'verbose_name': 'Продукт',
                'verbose_name_plural': 'Продукты',
                'db_table': 'products',
                'unique_together': {('name', 'model', 'release_date', 'supplier')},
            },
        ),
    ]
