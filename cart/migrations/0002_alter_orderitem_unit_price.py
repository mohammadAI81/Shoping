# Generated by Django 5.0.7 on 2024-08-02 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='unit_price',
            field=models.DecimalField(decimal_places=2, max_digits=6),
        ),
    ]