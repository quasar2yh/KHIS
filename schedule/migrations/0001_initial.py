# Generated by Django 4.2 on 2024-05-16 08:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Annual',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('practitioner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.practitioner')),
            ],
        ),
    ]
