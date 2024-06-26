# Generated by Django 4.2 on 2024-06-12 05:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('procedure', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProcedureFee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fee', models.DecimalField(decimal_places=2, max_digits=11)),
                ('effective_start', models.DateField()),
                ('effective_end', models.DateField()),
                ('updated', models.DateTimeField(auto_now=True)),
                ('procedure', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='procedure_fee', to='procedure.procedure')),
            ],
        ),
    ]
