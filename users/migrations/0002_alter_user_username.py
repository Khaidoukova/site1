# Generated by Django 5.0.1 on 2024-03-11 05:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(blank=True, max_length=150, null=True, unique=True, verbose_name='Ваш ник нейм'),
        ),
    ]
