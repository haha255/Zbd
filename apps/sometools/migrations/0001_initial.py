# Generated by Django 2.1.4 on 2020-01-14 16:53

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Calendar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=60, verbose_name='事件')),
                ('start', models.DateTimeField(blank=True, null=True, verbose_name='开始时间')),
                ('end', models.DateTimeField(blank=True, null=True, verbose_name='结束时间')),
                ('allday', models.BooleanField(default=False, verbose_name='全天')),
                ('content', models.TextField(blank=True, max_length=1000, null=True, verbose_name='描述')),
                ('isfinish', models.BooleanField(default=True, verbose_name='是否完成')),
                ('createtime', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建日期')),
            ],
            options={
                'verbose_name': '事件日历',
                'verbose_name_plural': '事件日历',
            },
        ),
        migrations.CreateModel(
            name='Dic_Event_Type',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='事件类型')),
                ('color', models.CharField(max_length=10, verbose_name='表示颜色')),
            ],
            options={
                'verbose_name': '事件类型',
                'verbose_name_plural': '事件类型',
            },
        ),
        migrations.AddField(
            model_name='calendar',
            name='type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='sometools.Dic_Event_Type', verbose_name='事件类型'),
        ),
    ]