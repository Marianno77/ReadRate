# Generated by Django 5.1.6 on 2025-03-05 21:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='admin',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
