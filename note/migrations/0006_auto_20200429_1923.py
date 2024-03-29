# Generated by Django 3.0.3 on 2020-04-29 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('note', '0005_auto_20200421_0046'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='slug',
            field=models.SlugField(blank=True, max_length=180),
        ),
        migrations.AlterField(
            model_name='category',
            name='description',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='category',
            name='keywords',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(blank=True, max_length=180),
        ),
        migrations.AlterField(
            model_name='note',
            name='description',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='note',
            name='keywords',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
