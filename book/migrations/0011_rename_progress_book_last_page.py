# Generated by Django 4.2.4 on 2023-11-27 07:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0010_book_progress_book_total_votes_book_total_wishlist'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='progress',
            new_name='last_page',
        ),
    ]
