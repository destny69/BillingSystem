# Generated by Django 5.1.3 on 2024-12-05 09:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='remaning_credit',
            new_name='total_credit',
        ),
        migrations.RenameField(
            model_name='customer',
            old_name='remaning_debit',
            new_name='total_debit',
        ),
    ]
