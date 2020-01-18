from django.shortcuts import render
from django.views.generic.base import View, TemplateView
from system.mixin import LoginRequiredMixin


class MyReportView(LoginRequiredMixin, TemplateView):

    template_name = 'dailyreport/myreport.html'
