# Generated by Django 3.0.5 on 2021-03-03 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0012_auto_20210301_1026'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='last_visits',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='num_visits',
            field=models.IntegerField(default=0),
        ),
    ]
