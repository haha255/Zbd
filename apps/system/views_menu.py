from django.views.generic import ListView
from .mixin import LoginRequiredMixin
from .models import Menu
from apps.custom import ZbdUpdateView, ZbdCreateView


class MenuCreateView(ZbdCreateView):
    model = Menu
    fields = '__all__'
    extra_context = dict(menu_all=Menu.objects.all())


class MenuListView(LoginRequiredMixin, ListView):
    model = Menu
    context_object_name = 'menu_all'


class MenuUpdateView(ZbdUpdateView):
    model = Menu
    fields = '__all__'
    template_name_suffix = '_update'
    extra_context = dict(menu_all=Menu.objects.all())
