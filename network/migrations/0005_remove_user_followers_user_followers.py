# Generated by Django 4.1.4 on 2023-04-09 22:48

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0004_user_followers_delete_follow'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='followers',
        ),
        migrations.AddField(
            model_name='user',
            name='followers',
            field=models.ManyToManyField(null=True, related_name='user_followers', to=settings.AUTH_USER_MODEL),
        ),
    ]
