# Generated by Django 5.0.6 on 2024-07-17 20:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0012_delete_businesscontact'),
    ]

    operations = [
        migrations.CreateModel(
            name='BusinessContact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(help_text='A valid phone number, please. This phone number is used for contact purposes if there is any enquiry.', max_length=20)),
                ('email', models.EmailField(help_text='A valid email address, please. This email is used for contact purposes if there is any enquiry.', max_length=255)),
                ('website', models.URLField(blank=True, help_text='A valid URL make sure to include http:// or https://.', max_length=255, null=True)),
                ('business', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='contact', to='business.businessprofile')),
            ],
        ),
    ]
