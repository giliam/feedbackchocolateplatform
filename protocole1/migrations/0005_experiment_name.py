# Generated by Django 3.0.3 on 2020-04-08 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('protocole1', '0004_result_finished'),
    ]

    operations = [
        migrations.AddField(
            model_name='experiment',
            name='name',
            field=models.CharField(default='experiment', max_length=150),
        ),
    ]