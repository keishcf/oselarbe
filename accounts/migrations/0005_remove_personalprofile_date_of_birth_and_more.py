# Generated by Django 5.0.6 on 2024-06-11 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_remove_personalprofile_headline_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='personalprofile',
            name='date_of_birth',
        ),
        migrations.RemoveField(
            model_name='personalprofile',
            name='pronouns',
        ),
        migrations.AddField(
            model_name='personalprofile',
            name='phone',
            field=models.CharField(blank=True, help_text='Your phone number', max_length=20, null=True, verbose_name='Phone'),
        ),
    ]
