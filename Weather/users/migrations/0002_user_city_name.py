# Generated by Django 4.2.16 on 2024-11-01 22:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='city_name',
            field=models.CharField(default='', max_length=50, verbose_name='City Name'),
        ),
    ]
