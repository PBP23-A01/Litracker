# Generated by Django 4.2.4 on 2023-12-17 08:55

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("book", "0019_remove_bookvotes_upvoted_by"),
        ("authentication", "0007_userprofile_books_userprofile_history_books_and_more"),
        ("review_book", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Review",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("comment", models.TextField()),
                (
                    "rating",
                    models.PositiveIntegerField(
                        default=0,
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(5),
                        ],
                    ),
                ),
                ("timestamp", models.DateTimeField(default=django.utils.timezone.now)),
                (
                    "book",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="book.book"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="authentication.userprofile",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="CommentLike",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "review",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="review_book.review",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="authentication.userprofile",
                    ),
                ),
            ],
        ),
    ]
