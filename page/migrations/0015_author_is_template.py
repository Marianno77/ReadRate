# Generated by Django 5.1.6 on 2025-03-12 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('page', '0014_book_is_template_delete_booktemplate'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='is_template',
            field=models.BooleanField(default=False),
        ),
    ]
