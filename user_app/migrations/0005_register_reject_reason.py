# Generated by Django 5.1.4 on 2024-12-27 04:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0004_remove_register_disease_register_disease'),
    ]

    operations = [
        migrations.AddField(
            model_name='register',
            name='reject_reason',
            field=models.TextField(default='', null=True),
        ),
    ]
