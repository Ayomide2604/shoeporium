# Generated by Django 5.1.5 on 2025-02-01 20:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_shoeimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='shoe',
            name='featured_image',
            field=models.ImageField(blank=True, null=True, upload_to='shoes'),
        ),
    ]
