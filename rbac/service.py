from django.shortcuts import HttpResponse,redirect,render
from django.views import View
from django.utils.safestring import mark_safe
import re
from rbacdemo import settings
from rbac import models
from django.db.models import Count
def initial_permission(request,user_id):
    """
    初始化权限，获取当前用户权限并添加到session中
    将当前用户权限信息转换为以下格式，并将其添加到session中
    {
        '/index.html':['GET','POST','DEL','EDIT'],
        '/detail-(\d+).html':['GET','POST','DEL','EDIT'],
    }

    :param request: 请求对象
    :param user_id: 当前用户id
    :return:
    """
    """初始化权限信息,格式处理好后，存在session"""
    roles = models.Role.objects.filter(users__user_id=user_id)
    p2a = models.Permission2Action2Role.objects.filter(role__in=roles).values(
        'permission__url',
        'action__code').distinct()

    user_permission_dict = {}
    for item in p2a:
        """
        user_permission_dict=
        {'product.html': ['GET'], 'order.html': ['POST', 'GET'], 'index.html': ['GET']}
        """
        if item['permission__url'] in user_permission_dict:
            user_permission_dict[item['permission__url']].append(item['action__code'])
        else:
            user_permission_dict[item['permission__url']] = [item['action__code']]
    print("登录存user权限session字典",user_permission_dict)

    #把用户权限按规定格式存在session中
    request.session[settings.RBAC_PERMISSION_SESSION_KEY] = user_permission_dict

    """初始化菜单信息，将菜单信息和权限信息添加到session中"""
    #所有菜单列表,注：转成list形式
    menu_list = list(models.Menu.objects.values('id','caption','parent_id'))

    #当前用户菜单列表
    menu_permission_list = list(models.Permission2Action2Role.objects.filter(role__in=roles,
                                                                             permission__menu__isnull=False).values(
        'permission__id',
        'permission__url',
        'permission__menu_id',
        'permission__caption', ).distinct())

    print("登录存user,session菜单",menu_permission_list)
    request.session[settings.RBAC_MENU_PERMISSION_SESSION_KEY] = {
        settings.RBAC_MENU_KEY:menu_list,#所有菜单列表，注：处理成列表形式
        settings.RBAC_MENU_PERMISSION_KEY:menu_permission_list #当前用户权限菜单列表，注：处理成列表形式
    }



