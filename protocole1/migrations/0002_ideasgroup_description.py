# Generated by Django 3.0.3 on 2020-04-02 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('protocole1', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ideasgroup',
            name='description',
            field=models.TextField(default=''),
        ),
    ]
