from django.views.generic import TemplateView
from .mixin import LoginRequiredMixin
from custom import ZbdCreateView, ZbdUpdateView
from .models import Role
from django.views.generic.base import View
from django.http import JsonResponse


class RoleView(LoginRequiredMixin, TemplateView):
    template_name = 'system/role.html'


class RoleCreateView(ZbdCreateView):
    model = Role
    fields = '__all__'


class RoleListView(LoginRequiredMixin, View):

    def get(self, request):
        fields = ['id', 'name', 'desc']
        ret = dict(data=list(Role.objects.values(*fields)))
        return JsonResponse(ret)


class RoleUpdateView(ZbdUpdateView):
    model = Role
    fields = '__all__'
    template_name_suffix = '_update'


class RoleDeleteView(LoginRequiredMixin, View):

    def post(self, request):
        ret = dict(result=False)
        if 'id' in request.POST and request.POST['id']:
            id_list = map(int, request.POST['id'].split(','))  # 多个ip用逗号隔开
            Role.objects.filter(id__in=id_list).delete()
            ret['result'] = True
        return JsonResponse(ret)
