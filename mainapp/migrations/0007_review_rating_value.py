# Generated by Django 2.2.5 on 2020-01-20 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0006_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='rating_value',
            field=models.IntegerField(default=0),
        ),
    ]