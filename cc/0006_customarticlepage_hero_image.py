# Generated by Django 5.1.2 on 2024-11-20 22:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0026_delete_uploadedimage'),
        ('website', '0005_hocapage'),
    ]

    operations = [
        migrations.AddField(
            model_name='customarticlepage',
            name='hero_image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image'),
        ),
    ]
