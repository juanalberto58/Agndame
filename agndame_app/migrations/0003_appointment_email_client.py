# Generated by Django 4.2.16 on 2024-09-30 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agndame_app', '0002_service_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='email_client',
            field=models.EmailField(default=1, max_length=254),
            preserve_default=False,
        ),
    ]
