# Generated by Django 3.0.3 on 2020-03-30 10:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('note', '0002_note'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='image',
            field=models.ImageField(blank=True, upload_to='pictures/'),
        ),
        migrations.AlterField(
            model_name='category',
            name='title',
            field=models.CharField(max_length=180),
        ),
        migrations.AlterField(
            model_name='note',
            name='image',
            field=models.ImageField(blank=True, upload_to='pictures/'),
        ),
        migrations.AlterField(
            model_name='note',
            name='title',
            field=models.CharField(max_length=180),
        ),
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('image', models.ImageField(blank=True, upload_to='pictures/')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='note.Note')),
            ],
        ),
    ]
