# Generated by Django 5.0.6 on 2024-06-06 10:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_remove_personalprofile_favorite_dish_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personalsocial',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='social', to='accounts.personalaccount'),
        ),
    ]
