# Generated by Django 4.2.11 on 2024-03-15 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_user_phone_alter_user_user_about_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dogs',
            name='dog_avatar',
            field=models.ImageField(blank=True, null=True, upload_to='dogs_photo', verbose_name='Аватар собаки (не более 1мб, 600х600px)'),
        ),
    ]
