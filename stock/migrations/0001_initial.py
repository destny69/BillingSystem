# Generated by Django 5.1.3 on 2024-12-04 13:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bill_no', models.PositiveIntegerField(unique=True)),
                ('date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('company', models.CharField(default=' ', max_length=50)),
                ('debit', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('credit', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('product_code', models.CharField(max_length=50, unique=True)),
                ('selling_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('cost_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='BillItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stock.bill')),
            ],
        ),
        migrations.AddField(
            model_name='bill',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stock.customer'),
        ),
        migrations.CreateModel(
            name='BillItemProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('rate', models.DecimalField(decimal_places=2, max_digits=10)),
                ('bill_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='stock.billitem')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stock.product')),
            ],
        ),
    ]