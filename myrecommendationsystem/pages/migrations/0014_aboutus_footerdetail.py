# Generated by Django 3.1.4 on 2021-06-09 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0013_auto_20210303_1339'),
    ]

    operations = [
        migrations.AddField(
            model_name='aboutus',
            name='footerdetail',
            field=models.TextField(default='Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.'),
        ),
    ]