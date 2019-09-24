# Generated by Django 2.1 on 2019-02-06 02:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device_type', models.CharField(max_length=50)),
                ('manufacturer', models.CharField(max_length=50)),
                ('device_model', models.CharField(max_length=50)),
                ('price', models.FloatField()),
                ('rental_details', models.CharField(max_length=400)),
                ('is_available', models.BooleanField(default=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True, verbose_name='Created Time')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('details', models.CharField(max_length=400)),
                ('transaction_time', models.DateTimeField(auto_now=True, null=True, verbose_name='Time of Transaction Initiation')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=20)),
            ],
        ),
        migrations.AddField(
            model_name='transaction',
            name='buyer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='buyer', to='app.User'),
        ),
        migrations.AddField(
            model_name='transaction',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='app.Device'),
        ),
        migrations.AddField(
            model_name='transaction',
            name='seller',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='seller', to='app.User'),
        ),
        migrations.AddField(
            model_name='device',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='app.User'),
        ),
    ]
