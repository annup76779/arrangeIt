# Generated by Django 4.2.2 on 2023-07-10 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='additional',
            field=models.TextField(blank=True, null=True),
        ),
    ]
