# Generated by Django 4.1.3 on 2023-03-12 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_alter_post_like_check'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='like_check',
            field=models.IntegerField(default=50),
        ),
    ]
