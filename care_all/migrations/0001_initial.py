# Generated by Django 2.2 on 2020-08-04 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Elder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_photo', models.ImageField(blank=True, upload_to='profile/user_profile_photo/')),
                ('name', models.CharField(blank=True, max_length=150)),
                ('age', models.PositiveIntegerField(blank=True)),
                ('status', models.CharField(choices=[('Yes', 'Available'), ('No', 'Un-Available')], default='Available', max_length=20)),
                ('funds', models.IntegerField(blank=True)),
                ('bio', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Youngster',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_photo', models.ImageField(blank=True, upload_to='profile/user_profile_photo/')),
                ('name', models.CharField(blank=True, default='Anonymous', max_length=150)),
                ('age', models.PositiveIntegerField(blank=True)),
                ('elders_in_care', models.IntegerField(blank=True)),
                ('bio', models.TextField(blank=True)),
            ],
        ),
    ]
