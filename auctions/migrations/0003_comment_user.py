# Generated by Django 4.1.3 on 2022-12-04 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_alter_auction_listing_bid_closed'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.TextField(default='Enter some user'),
        ),
    ]
