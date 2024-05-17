# Generated by Django 4.2 on 2024-05-17 08:49

import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('use', models.CharField(choices=[('Home', 'Home'), ('Work', 'Work'), ('Temp', 'Temp'), ('Old', 'Old'), ('Billing', 'Billing')], max_length=10)),
                ('text', models.TextField()),
                ('city', models.CharField(max_length=100)),
                ('postal_code', models.CharField(max_length=20)),
                ('country', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='ContactPoint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('system', models.CharField(choices=[('Phone', 'Phone'), ('Fax', 'Fax'), ('Email', 'Email'), ('Pager', 'Pager'), ('URL', 'URL'), ('SMS', 'SMS'), ('Other', 'Other')], max_length=10)),
                ('value', models.TextField(unique=True)),
                ('use', models.CharField(choices=[('Home', 'Home'), ('Work', 'Work'), ('Temp', 'Temp'), ('Old', 'Old'), ('Mobile', 'Mobile')], max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='HumanName',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('family', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other'), ('Unknown', 'Unknown')], max_length=10)),
                ('birth_date', models.DateTimeField(blank=True, null=True)),
                ('blood_type', models.CharField(blank=True, choices=[('RH+A', 'RH+A'), ('RH-A', 'RH-A'), ('RH+B', 'RH+B'), ('RH-B', 'RH-B'), ('RH+O', 'RH+O'), ('RH-O', 'RH-O'), ('RH+AB', 'RH+AB'), ('RB-AB', 'RB-AB')], max_length=10, null=True)),
                ('marital_status', models.BooleanField(blank=True)),
                ('allergies', models.CharField(blank=True, max_length=255)),
                ('address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account.address')),
                ('name', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account.humanname')),
                ('telecom', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account.contactpoint')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RelatedPerson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other'), ('Unknown', 'Unknown')], max_length=10)),
                ('birth_date', models.DateTimeField(blank=True, null=True)),
                ('address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account.address')),
                ('name', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account.humanname')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.patient')),
                ('telecom', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account.contactpoint')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Practitioner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other'), ('Unknown', 'Unknown')], max_length=10)),
                ('birth_date', models.DateTimeField(blank=True, null=True)),
                ('license_type', models.CharField(max_length=10)),
                ('license_number', models.CharField(max_length=100)),
                ('role', models.CharField(choices=[('Physician', 'Physician'), ('Assistant', 'Assistant')], max_length=10)),
                ('rank', models.IntegerField()),
                ('address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account.address')),
                ('department', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account.department')),
                ('name', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account.humanname')),
                ('telecom', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account.contactpoint')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('subject', models.CharField(max_length=20)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('patient', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account.patient')),
                ('practitioner', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account.practitioner')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
