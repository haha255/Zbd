# Generated by Django 2.2.6 on 2020-01-12 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0002_auto_20191026_1839'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='menu',
            options={'ordering': ['number'], 'verbose_name': '菜单', 'verbose_name_plural': '菜单'},
        ),
        migrations.AddField(
            model_name='menu',
            name='number',
            field=models.FloatField(blank=True, null=True, verbose_name='编号'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='tel',
            field=models.CharField(default='', max_length=11, verbose_name='座机'),
        ),
    ]
