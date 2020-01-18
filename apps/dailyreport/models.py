from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone


User = get_user_model()  # 取用户模型


class EventType(models.Model):
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


class DailyReport(models.Model):
    """
    事件日历
    """
    title = models.TextField(max_length=1000, verbose_name="日程")
    type = models.ForeignKey('EventType', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='日程类型')
    start = models.DateTimeField(null=True, blank=True, verbose_name='开始时间')
    end = models.DateTimeField(null=True, blank=True, verbose_name='结束时间')
    allday = models.BooleanField(default=False, verbose_name='全天')
    user = models.ForeignKey(User, related_name='report_user', on_delete=models.DO_NOTHING, default='')
    participants = models.ManyToManyField(User, related_name='participants', blank=True)
    addtime = models.DateTimeField(default=timezone.now, verbose_name='创建时间')

    class Meta:
        ordering = ['start', '-end']
        verbose_name = "日历日程"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title
