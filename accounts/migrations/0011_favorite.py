# Generated by Django 5.0.6 on 2024-06-24 21:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_remove_personalprofile_gender'),
        ('business', '0002_rename_date_posted_businessreview_created_at_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('from_personal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to='accounts.personalaccount')),
                ('to_business', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorited', to='business.businessprofile')),
            ],
            options={
                'unique_together': {('from_personal', 'to_business')},
            },
        ),
    ]
