# Generated by Django 3.2.18 on 2023-03-06 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='image',
            field=models.ImageField(blank=True, upload_to='images/'),
        ),
    ]
