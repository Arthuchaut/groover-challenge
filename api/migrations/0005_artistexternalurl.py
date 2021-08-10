# Generated by Django 3.2.6 on 2021-08-10 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_album'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArtistExternalURL',
            fields=[
                ('external_url_id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
            ],
            options={
                'verbose_name': 'artist external url',
                'verbose_name_plural': 'artist external urls',
                'db_table': 'artist_external_url',
            },
        ),
    ]
