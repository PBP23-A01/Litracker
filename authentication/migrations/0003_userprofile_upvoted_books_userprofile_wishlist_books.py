# Generated by Django 4.2.6 on 2023-10-28 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0003_book_total_votes'),
        ('authentication', '0002_userprofile_books'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='upvoted_books',
            field=models.ManyToManyField(blank=True, related_name='upvoters', to='book.book'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='wishlist_books',
            field=models.ManyToManyField(blank=True, related_name='wishlists', to='book.book'),
        ),
    ]
