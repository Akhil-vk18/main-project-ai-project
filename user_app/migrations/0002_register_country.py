# Generated by Django 5.1.4 on 2024-12-19 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='register',
            name='country',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
