# Generated by Django 3.2.18 on 2023-03-12 18:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0002_auto_20230309_2158'),
        ('profiles', '0002_preference'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='preference',
            unique_together={('profile', 'genre')},
        ),
    ]
