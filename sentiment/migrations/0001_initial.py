# Generated by Django 4.1.4 on 2022-12-18 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Sentiment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('sentiment', models.TextField()),
                ('created', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]