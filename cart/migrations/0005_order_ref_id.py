# Generated by Django 5.0.7 on 2024-08-06 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0004_order_authority'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='ref_id',
            field=models.PositiveIntegerField(blank=True, max_length=10, null=True),
        ),
    ]
