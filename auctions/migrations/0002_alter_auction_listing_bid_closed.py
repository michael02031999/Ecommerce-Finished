# Generated by Django 4.1.3 on 2022-12-04 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction_listing',
            name='bid_closed',
            field=models.CharField(default='open', max_length=500),
        ),
    ]
