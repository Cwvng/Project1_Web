# Generated by Django 4.1.3 on 2023-03-13 04:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_post_user_wishlist_alter_post_like_check'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='favourite',
        ),
        migrations.AlterField(
            model_name='post',
            name='like_check',
            field=models.IntegerField(default=72),
        ),
    ]
