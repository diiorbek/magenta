# Generated by Django 5.1.6 on 2025-02-28 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Magenta', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='description',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='category',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='category_images'),
        ),
    ]
