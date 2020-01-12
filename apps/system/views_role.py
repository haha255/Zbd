import json
from django.views.generic import TemplateView
from .mixin import LoginRequiredMixin
from custom import ZbdCreateView, ZbdUpdateView
from .models import Role, Menu
from django.views.generic.base import View
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth import get_user_model


User = get_user_model()


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


class Role2UserView(LoginRequiredMixin, View):
    """
    角色关联用户
    """
    def get(self, request):
        if 'id' in request.GET and request.GET['id']:
            role = get_object_or_404(Role, pk=int(request.GET['id']))
            added_users = role.userprofile_set.all()  # 用外键反向查找所有用户集
            all_users = User.objects.all()  # 所有用户
            un_add_users = set(all_users).difference(added_users)  # 取差集
            ret = dict(role=role, added_users=added_users, un_add_users=list(un_add_users))
        return render(request, 'system/role_role2user.html', ret)

    def post(self, request):
        res = dict(result=False)
        id_list = None
        role = get_object_or_404(Role, pk=int(request.POST['id']))
        if 'to' in request.POST and request.POST['to']:
            id_list = map(int, request.POST.getlist('to', []))
        role.userprofile_set.clear()  # 清空原先的所有绑定信息
        if id_list:
            for user in User.objects.filter(id__in=id_list):
                role.userprofile_set.add(user)
        res['result'] = True
        return JsonResponse(res)


class Role2MenuView(LoginRequiredMixin, View):
    """
    角色绑定菜单
    """
    # 用于返回权限绑定的模板页和选中的角色组实例
    def get(self, request):
        if 'id' in request.GET and request.GET['id']:
            role = get_object_or_404(Role, pk=int(request.GET['id']))
            ret = dict(role=role)
            return render(request, 'system/role_role2menu.html', ret)
    # 用于接收权限配置信息

    def post(self, request):
        res = dict(result=False)
        role = get_object_or_404(Role, pk=int(request.POST['id']))
        tree = json.loads(self.request.POST['tree'])
        # 清除原有的权限信息
        role.permissions.clear()
        # 重新添加菜单
        for menu in tree:
            if menu['checked'] is True:
                menu_checked = get_object_or_404(Menu, pk=int(menu['id']))
                role.permissions.add(menu_checked)
        res['result'] = True
        return JsonResponse(res)


class Role2MenuListView(LoginRequiredMixin, View):
    """
    zTree在生成带单树状结构时，会通过该接口获取菜单列表数据
    """
    def get(self, request):
        fields = ['id', 'name', 'parent']
        if 'id' in request.GET and request.GET['id']:
            role = Role.objects.get(id=request.GET.get('id'))
            role_menus = role.permissions.values(*fields)
            ret = dict(data=list(role_menus))
        else:
            menus = Menu.objects.all()
            ret = dict(data=list(menus.values(*fields)))
        return JsonResponse(ret)
