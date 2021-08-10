# Generated by Django 3.2.6 on 2021-08-10 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_artist'),
    ]

    operations = [
        migrations.CreateModel(
            name='Market',
            fields=[
                ('market_id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('coutry_code', models.CharField(max_length=2)),
            ],
            options={
                'verbose_name': 'market',
                'verbose_name_plural': 'markets',
                'db_table': 'market',
            },
        ),
    ]