# Generated by Django 2.1.4 on 2020-01-15 11:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sometools', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='calendar',
            options={'ordering': ['start', '-end'], 'verbose_name': '事件日历', 'verbose_name_plural': '事件日历'},
        ),
    ]