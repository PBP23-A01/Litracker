# Generated by Django 4.2.4 on 2023-12-12 20:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("book", "0016_bookvotes_upvoted_by"),
    ]

    operations = [
        migrations.RemoveField(model_name="bookvotes", name="upvoted_by",),
    ]