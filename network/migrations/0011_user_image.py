# Generated by Django 4.1.4 on 2023-05-16 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0010_likepost'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
