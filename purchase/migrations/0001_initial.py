# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2020-12-04 05:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PurchaseModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('purchaser_name', models.CharField(max_length=50)),
                ('quantity', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='PurchaseStatusModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('open', 'Open'), ('verified', 'Verified'), ('dispatched', 'Dispatched'), ('delivered', 'Delivered')], max_length=25)),
                ('created_at', models.DateTimeField(db_index=True)),
                ('purchase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='purchase.PurchaseModel')),
            ],
        ),
    ]
