# Generated by Django 4.2 on 2024-05-17 05:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0002_schedule'),
    ]

    operations = [
        migrations.AddField(
            model_name='annual',
            name='reason',
            field=models.TextField(blank=True, null=True),
        ),
    ]