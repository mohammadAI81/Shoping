# Generated by Django 5.1 on 2024-08-12 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_remove_comment_reply_comment_id_reply'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='image',
            field=models.ImageField(blank=True, upload_to='cover/blog/%Y/'),
        ),
    ]
