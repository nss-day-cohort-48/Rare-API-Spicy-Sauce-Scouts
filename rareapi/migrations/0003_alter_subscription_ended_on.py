# Generated by Django 3.2.6 on 2021-08-18 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rareapi', '0002_subscription'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='ended_on',
            field=models.DateField(null=True),
        ),
    ]