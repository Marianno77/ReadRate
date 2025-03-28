# Generated by Django 5.1.6 on 2025-02-26 17:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('page', '0004_remove_book_author_obj_alter_book_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='author_obj',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='page.author'),
        ),
        migrations.AlterField(
            model_name='book',
            name='author',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
