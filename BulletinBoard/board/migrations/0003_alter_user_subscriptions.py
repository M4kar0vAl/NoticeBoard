# Generated by Django 5.0.2 on 2024-02-26 17:52

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0002_alter_user_subscriptions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='subscriptions',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=2), default=list, size=10),
        ),
    ]
