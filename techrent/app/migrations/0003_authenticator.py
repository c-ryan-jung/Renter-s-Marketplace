# Generated by Django 2.1 on 2019-04-01 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20190206_1948'),
    ]

    operations = [
        migrations.CreateModel(
            name='Authenticator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('authenticator', models.CharField(max_length=100)),
                ('date_created', models.DateField()),
            ],
        ),
    ]
