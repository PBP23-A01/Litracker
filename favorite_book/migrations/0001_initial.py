# Generated by Django 5.0 on 2023-12-20 10:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authentication', '0007_userprofile_books_userprofile_history_books_and_more'),
        ('book', '0019_remove_bookvotes_upvoted_by'),
    ]

    operations = [
        migrations.CreateModel(
            name='WishlistBook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.book')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.userprofile')),
            ],
        ),
    ]
