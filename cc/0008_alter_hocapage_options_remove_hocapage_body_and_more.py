# Generated by Django 5.1.2 on 2024-11-22 09:26

import django.db.models.deletion
import modelcluster.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0094_alter_page_locale'),
        ('website', '0007_hocapage_featured_hoca'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='hocapage',
            options={'verbose_name': 'Doctors Page'},
        ),
        migrations.RemoveField(
            model_name='hocapage',
            name='body',
        ),
        migrations.RemoveField(
            model_name='hocapage',
            name='coderedpage_ptr',
        ),
        migrations.RemoveField(
            model_name='hocapage',
            name='featured_hoca',
        ),
        migrations.AddField(
            model_name='hocapage',
            name='page_ptr',
            field=models.OneToOneField(auto_created=True, default=22, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page'),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='HocaPageHoca',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hoca', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='website.hoca')),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='hoca_links', to='website.hocapage')),
            ],
        ),
    ]