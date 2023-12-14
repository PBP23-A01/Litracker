# Generated by Django 4.2.4 on 2023-12-12 20:51

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("book", "0017_remove_bookvotes_upvoted_by"),
    ]

    operations = [
        migrations.AddField(
            model_name="bookvotes",
            name="upvoted_by",
            field=models.ManyToManyField(
                blank=True, related_name="users", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
