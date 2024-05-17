<<<<<<< HEAD
# Generated by Django 4.2 on 2024-05-16 10:59
=======
# Generated by Django 4.2 on 2024-05-17 02:21
>>>>>>> a42aa7bf09e55cbe470a84a3babc339687b656f8

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField()),
                ('syptom', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField()),
                ('department', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account.department')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.patient')),
                ('practitioner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account.practitioner')),
            ],
        ),
    ]
