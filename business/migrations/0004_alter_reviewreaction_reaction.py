# Generated by Django 5.0.6 on 2024-06-27 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0003_reviewreaction_delete_reviewvote'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reviewreaction',
            name='reaction',
            field=models.CharField(choices=[('helpful', 'Helpful'), ('appriciate', 'Appriciate')], max_length=10),
        ),
    ]
