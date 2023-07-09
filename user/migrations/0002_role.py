# Generated by Django 4.2.2 on 2023-07-09 16:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('add_time_table', models.BooleanField(default=False)),
                ('update_status', models.BooleanField(default=False)),
                ('date_of_creating', models.DateTimeField(auto_now_add=True)),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_role', to='user.organizationuser')),
            ],
        ),
    ]