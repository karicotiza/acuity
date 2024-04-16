# Generated by Django 5.0.4 on 2024-04-15 12:43

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Logs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.GenericIPAddressField(protocol='IPv4')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('hash', models.CharField(max_length=64, validators=[django.core.validators.MinLengthValidator(64)])),
            ],
        ),
    ]
