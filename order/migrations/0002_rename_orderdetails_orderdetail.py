# Generated by Django 4.0.1 on 2022-02-02 12:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='OrderDetails',
            new_name='OrderDetail',
        ),
    ]
