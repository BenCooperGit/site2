# Generated by Django 3.0.14 on 2022-08-21 19:24

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_auto_20220821_2010'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='start_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]