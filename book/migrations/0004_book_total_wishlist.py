# Generated by Django 4.2.6 on 2023-10-29 05:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0003_book_total_votes'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='total_wishlist',
            field=models.IntegerField(default=0),
        ),
    ]