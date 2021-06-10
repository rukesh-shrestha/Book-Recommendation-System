# Generated by Django 3.1.4 on 2021-02-24 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0005_aboutus'),
    ]

    operations = [
        migrations.CreateModel(
            name='login',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descriptions', models.TextField(default='People vary in terms of their physical appearance and personalities, and the words that are used to describe them are just as varied. Some words are better suited to describing the physical appearance of someone, some are best used to describe the person’s style, and others are ideal for describing the person’s character traits.', max_length=500)),
            ],
        ),
    ]
