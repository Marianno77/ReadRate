# Generated by Django 5.1.6 on 2025-03-08 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('page', '0010_alter_userfollowauthor_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='category',
            field=models.CharField(choices=[('Fantastyka', 'Fantastyka'), ('Science Fiction', 'Science Fiction'), ('Romans', 'Romans'), ('Thriller', 'Thriller'), ('Tajemnica', 'Tajemnica'), ('Kryminał', 'Kryminał'), ('Horror', 'Horror'), ('Biografia', 'Biografia'), ('Historia', 'Historia'), ('Manga', 'Manga'), ('Religia', 'Religia'), ('Komiks', 'Komiks'), ('Przygoda', 'Przygoda'), ('Psychologia', 'Psychologia'), ('Komedia', 'Komedia'), ('Dramat', 'Dramat'), ('Filozofia', 'Filozofia')], max_length=50),
        ),
        migrations.AlterField(
            model_name='review',
            name='review_text',
            field=models.TextField(blank=True, null=True),
        ),
    ]
