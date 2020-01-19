from django.shortcuts import render, get_object_or_404
from django.views.generic.base import View, TemplateView
from system.mixin import LoginRequiredMixin
from django.http import JsonResponse
from .models import EventType, DailyReport
from .forms import EventCreateForm
from django.contrib.auth import get_user_model
from django.db.models import Q
import datetime
import re


User = get_user_model()


class TestView(LoginRequiredMixin, TemplateView):

    template_name = 'mydesk/dailyreport/test.html'


class MyDeskView(LoginRequiredMixin, TemplateView):

    template_name = 'mydesk/index.html'


class MyReportView(LoginRequiredMixin, TemplateView):

    template_name = 'mydesk/dailyreport/myreport.html'


class EventCreateView(LoginRequiredMixin, View):

    def get(self, request):
        start = end = None
        if 'start' in request.GET and request.GET['start']:
            start = request.GET['start']
            start = ' '.join(start.split('T'))  # 目的是为了将'YYYY-MM-DDThh:mm'转换为'YYYY-MM-DD hh:mm'
        if 'end' in request.GET and request.GET['end']:
            end = request.GET['end']
            end = ' '.join(end.split('T'))  # 同start
        ret = {
            'participants': User.objects.exclude(username__in=['admin', ]),  # 暂时不考虑不是一个部门的人员
            'types': EventType.objects.all(),
            'start': start,
            'end': end
        }
        return render(request, 'mydesk/dailyreport/report_create.html', ret)

    def post(self, request):
        event_create_form = EventCreateForm(request.POST)
        if event_create_form.is_valid():
            event_create_form.save()  # 提交
            ret = {'result': True}
        else:
            pattern = '<li>.*?<ul class=.*?><li>(.*?)</li>'
            errors = str(event_create_form.errors)
            event_create_form_errors = re.findall(pattern, errors)
            ret = {
                'result': False,
                'event_create_form_errors': event_create_form_errors[0]
            }
        return JsonResponse(ret)


class EventListView(LoginRequiredMixin, View):

    def post(self, request):
        # get方法取得日历事件
        fields = ['id', 'type', 'title', 'start', 'end', 'allday', 'type__color']
        start = end = None
        if 'start' in request.POST and request.POST['start']:
            start = datetime.datetime.strptime(request.POST['start'], '%Y-%m-%dT%H:%M:%S')
        if 'end' in request.POST and request.POST['end']:
            end = datetime.datetime.strptime(request.POST['end'], '%Y-%m-%dT%H:%M:%S')
        if start and end:
            qs = DailyReport.objects.filter(start__gte=start).filter(end__lte=end).values(*fields)
        elif start:
            qs = DailyReport.objects.filter(start__gte=start).values(*fields)
        elif end:
            qs = DailyReport.objects.filter(end__lte=end).values(*fields)
        else:
            qs = DailyReport.objects.values(*fields)
        ret = dict(data=list(qs))  # 传一个列表，用于取得想要的字段
        return JsonResponse(ret)


class EventDetailView(LoginRequiredMixin, View):
    """
    日程详情:用于展示日程或者修改、删除日程
    """
    def get(self, request):
        ret = dict()
        if 'id' in request.GET and request.GET['id']:
            report = get_object_or_404(DailyReport, pk=int(request.GET['id']))
            ret = {
                'report': report,
                'user_all': User.objects.exclude(username__in=['admin', ]),
                'types': EventType.objects.all(),
            }
        return render(request, 'mydesk/dailyreport/report_detail.html', ret)

    def post(self, request):
        res = dict(result=False)
        if 'del_id' in request.POST and request.POST['del_id']:
            DailyReport.objects.filter(id=int(request.POST['del_id'])).delete()
            res['result'] = True
            return JsonResponse(res)

        if 'id' in request.POST and request.POST['id']:
            report = get_object_or_404(DailyReport, pk=int(request.POST['id']))
            report_form = EventCreateForm(request.POST, instance=report)
            if report_form.is_valid():
                report_form.save()
                res['result'] = True
        return JsonResponse(res)
