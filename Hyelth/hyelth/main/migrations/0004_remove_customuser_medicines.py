# Generated by Django 5.1.2 on 2025-05-19 17:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_alter_customuser_medicines'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='medicines',
        ),
    ]
