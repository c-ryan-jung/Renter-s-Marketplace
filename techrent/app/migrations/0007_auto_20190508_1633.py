# Generated by Django 2.1 on 2019-05-08 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_recommendation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recommendation',
            name='item_id',
            field=models.CharField(max_length=50),
        ),
    ]
