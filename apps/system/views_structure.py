import json
from django.views.generic.base import TemplateView, View
from .mixin import LoginRequiredMixin
from django.shortcuts import render, HttpResponse, get_object_or_404
from .forms import StructureForm
from .models import Structure
from django.http import JsonResponse
from django.contrib.auth import get_user_model


User = get_user_model()  # 取得user模型


class Structure2UserView(LoginRequiredMixin, View):

    def get(self, request):
        if 'id' in request.GET and request.GET['id']:
            # 通过id获取需要绑定用户的组织架构实例
            structure = get_object_or_404(Structure, pk=int(request.GET['id']))
            # 通过外键的反向查找(_set)，找到已经绑定到该组织架构的所有用户信息
            added_users = structure.userprofile_set.all()
            # 查找系统中所有用户信息，User=get_user_object()使用自定义用户都是通过这种模式
            all_users = User.objects.all()
            # 同集合获取差集set().difference()，得出未绑定的用户
            un_add_users = set(all_users).difference(added_users)
            # 将这些数据返回给前端，用于渲染数据，形成一个复选框。左边为待选用户，右边是已经绑定用户
            ret = dict(structure=structure, added_users=added_users, un_add_users=un_add_users)
        return render(request, 'system/structure/structure_user.html', ret)

    def post(self, request):
        res = dict(result=False)
        id_list = None
        # 通过ID获取structure实例
        structure = get_object_or_404(Structure, pk=int(request.POST['id']))
        # 获取需要绑定到structure实例的用户id
        if 'to' in request.POST and request.POST.getlist('to', []):
            id_list = map(int, request.POST.getlist('to', []))  # 转换为map类型
        # 清空组织架构原有用户绑定信息
        structure.userprofile_set.clear()
        if id_list:
            # 绑定新的用户数据
            for user in User.objects.filter(id__in=id_list):
                structure.userprofile_set.add(user)
        res['result'] = True
        return JsonResponse(res)


class StructureView(LoginRequiredMixin, TemplateView):
    template_name = 'system/structure/structure.html'


class StructureCreateView(LoginRequiredMixin, View):

    def get(self, request):
        ret = dict(structure_all=Structure.objects.all())
        if 'id' in request.GET and request.GET['id']:
            structure = get_object_or_404(Structure, pk=request.GET['id'])
            ret['structure'] = structure
        return render(request, 'system/structure/structure_create.html', ret)

    def post(self, request):
        res = dict(result=False)
        if 'id' in request.POST and request.POST['id']:
            structure = get_object_or_404(Structure, pk=request.POST['id'])
        else:  # 如果ID不存在，为新增，使用Null模型传递instance参数，调用save新建
            structure = Structure()
        stru_form = StructureForm(request.POST, instance=structure)
        if stru_form.is_valid():
            stru_form.save()
            res['result'] = True
        return HttpResponse(json.dumps(res), content_type='application/json')


class StructureListView(LoginRequiredMixin, View):

    def get(self, request):
        fields = ['id', 'name', 'type', 'parent__name']  # parent__name外键获取对应字表的name属性内容
        ret = dict(data=list(Structure.objects.values(*fields)))  # 传一个列表，用于取得想要的字段
        return HttpResponse(json.dumps(ret), content_type='application/json')
        #return JsonResponse(ret)


class StructureDeleteView(LoginRequiredMixin, View):

    def post(self, request):
        ret = dict(result=False)
        if 'id' in request.POST and request.POST['id']:
            id_list = map(int, request.POST['id'].split(','))  # 多个一起删除的情形
            Structure.objects.filter(id__in=id_list).delete()  # 全部删除
            ret['result'] = True
        return JsonResponse(ret)
