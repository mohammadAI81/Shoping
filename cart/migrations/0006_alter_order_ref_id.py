# Generated by Django 5.0.7 on 2024-08-06 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0005_order_ref_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='ref_id',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]