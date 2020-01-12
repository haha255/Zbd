import re
from django.utils.deprecation import MiddlewareMixin


class MenuCollection(MiddlewareMixin):

    def get_user(self, request):
        return request.user

    def get_menu_from_role(self, request, user=None):  # 从数据库中返回menu的行，形成一个列表
        if user is None:
            user = self.get_user(request)
        try:
            menus = user.roles.values(
                'permissions__id',
                'permissions__name',
                'permissions__url',
                'permissions__icon',
                'permissions__code',
                'permissions__parent'
            ).distinct()
            return [menu for menu in menus if menu['permissions__id'] is not None]
        except AttributeError:
            return None

    def get_permission_url(self, request):  # 获取用户有权限访问的url，存在一个列表中备查
        role_menus = self.get_menu_from_role(request)
        if role_menus is not None:
            permission_url_list = [menu['permissions__url'] for menu in role_menus]
            return permission_url_list

    def get_permission_menu(self, request):  # 获取用户有权访问的菜单行。
        permission_menu_list = []
        role_menus = self.get_menu_from_role(request)
        if role_menus is not None:
            for item in role_menus:
                menu = {
                    'id': item['permissions__id'],
                    'name': item['permissions__name'],
                    'url': item['permissions__url'],
                    'icon': item['permissions__icon'],
                    'code': item['permissions__code'],
                    'parent': item['permissions__parent'],
                    'status': False,  # 标识头部一级菜单的选中状态，模式为未选中。
                    'sub_menu': [],  # 用于存放下级菜单数据。
                }
                permission_menu_list.append(menu)
            return permission_menu_list

    def get_top_reveal_menu(self, request):  # 获取头部导航和侧边栏导航数据，根据层级进行组合
        top_menu = []
        permission_menu_dict = {}
        request_url = request.path_info
        permission_menu_list = self.get_permission_menu(request)
        if permission_menu_list is not None:
            for menu in permission_menu_list:
                url = menu['url']
                if url and re.match(url, request_url):
                    menu['status'] = True
                if menu['parent'] is None:
                    top_menu.insert(0, menu)
                permission_menu_dict[menu['id']] = menu
            menu_data = []
            for i in permission_menu_dict:
                if permission_menu_dict[i]['parent']:
                    pid = permission_menu_dict[i]['parent']
                    parent_menu = permission_menu_dict[pid]
                    parent_menu['sub_menu'].append(permission_menu_dict[i])
                else:
                    menu_data.append(permission_menu_dict[i])
            if [menu['sub_menu'] for menu in menu_data if menu['url'] in request_url]:
                reveal_menu = [menu['sub_menu'] for menu in menu_data if menu['url'] in request_url][0]
            else:
                reveal_menu = None
            return top_menu, reveal_menu

    def process_request(self, request):  # 将request请求传递给view前执行，所有整理组合好的菜单数据写入request。
        if self.get_top_reveal_menu(request):
            request.top_menu, request.reveal_menu = self.get_top_reveal_menu(request)
            request.permission_url_list = self.get_permission_url(request)
