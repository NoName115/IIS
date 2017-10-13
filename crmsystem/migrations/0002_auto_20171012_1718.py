# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-12 15:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crmsystem', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=150)),
                ('street_number', models.IntegerField()),
                ('street_name', models.CharField(max_length=150)),
                ('email', models.EmailField(max_length=254)),
                ('telephone_number', models.CharField(max_length=50)),
                ('some_date', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.DeleteModel(
            name='BlogPost',
        ),
    ]
