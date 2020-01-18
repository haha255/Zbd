from django.db import models
from django.utils import timezone


class Dic_Event_Type(models.Model):
    """
    事件类型，记录事件类型的字典，包括事件的颜色，为后期显示和统计使用
    """
    name = models.CharField(max_length=20, verbose_name='事件类型')
    color = models.CharField(max_length=10, verbose_name='表示颜色')

    class Meta:
        verbose_name = '事件类型'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


class Calendar(models.Model):
    """
    事件日历
    """
    title = models.CharField(max_length=60, verbose_name="事件")
    type = models.ForeignKey('Dic_Event_Type', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='事件类型')
    start = models.DateTimeField(null=True, blank=True, verbose_name='开始时间')
    end = models.DateTimeField(null=True, blank=True, verbose_name='结束时间')
    allday = models.BooleanField(default=False, verbose_name='全天')
    content = models.TextField(max_length=1000, null=True, blank=True, verbose_name='描述')
    isfinish = models.BooleanField(default=True, verbose_name='是否完成')
    createtime = models.DateTimeField(default=timezone.now, verbose_name='创建日期')

    class Meta:
        ordering = ['start', '-end']
        verbose_name = "事件日历"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title
