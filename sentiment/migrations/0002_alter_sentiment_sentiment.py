# Generated by Django 4.1.4 on 2022-12-18 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sentiment', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sentiment',
            name='sentiment',
            field=models.CharField(max_length=100),
        ),
    ]
