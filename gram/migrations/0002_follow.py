# Generated by Django 4.0.5 on 2022-06-06 00:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gram', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=255)),
                ('follower', models.CharField(max_length=255)),
            ],
        ),
    ]
