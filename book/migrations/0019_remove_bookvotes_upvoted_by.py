# Generated by Django 4.2.4 on 2023-12-14 17:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("book", "0018_bookvotes_upvoted_by"),
    ]

    operations = [
        migrations.RemoveField(model_name="bookvotes", name="upvoted_by",),
    ]
