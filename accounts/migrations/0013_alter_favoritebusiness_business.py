# Generated by Django 5.0.6 on 2024-06-24 21:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_favoritebusiness_delete_favorite'),
        ('business', '0002_rename_date_posted_businessreview_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favoritebusiness',
            name='business',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorite_of', to='business.businessprofile'),
        ),
    ]
