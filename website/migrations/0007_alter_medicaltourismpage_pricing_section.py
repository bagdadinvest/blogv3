# Generated by Django 5.1.2 on 2024-11-26 05:37

import wagtail.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0006_medicaltourismpage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicaltourismpage',
            name='pricing_section',
            field=wagtail.fields.StreamField([('pricing_item', 6)], blank=True, block_lookup={0: ('wagtail.blocks.CharBlock', (), {'label': 'Package Title', 'required': True}), 1: ('wagtail.blocks.CharBlock', (), {'label': 'Price', 'required': True}), 2: ('wagtail.blocks.CharBlock', (), {'label': 'Feature'}), 3: ('wagtail.blocks.ListBlock', (2,), {'label': 'Features List'}), 4: ('wagtail.blocks.CharBlock', (), {'label': 'Call to Action Label', 'required': True}), 5: ('wagtail.blocks.URLBlock', (), {'label': 'Call to Action URL', 'required': True}), 6: ('wagtail.blocks.StructBlock', [[('title', 0), ('price', 1), ('features', 3), ('cta_label', 4), ('cta_url', 5)]], {'label': 'Pricing Item'})}, verbose_name='Pricing Section'),
        ),
    ]