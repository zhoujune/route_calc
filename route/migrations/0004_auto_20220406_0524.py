# Generated by Django 3.1.4 on 2022-04-06 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('route', '0003_auto_20220403_1844'),
    ]

    operations = [
        migrations.AlterField(
            model_name='route',
            name='code',
            field=models.CharField(default='', max_length=50, verbose_name='route code'),
        ),
    ]
