import os
import re
from rbacdemo import settings
from django import template
from django.utils.safestring import mark_safe


register = template.Library()
def process_menu_tree_data(request):
    all_menu_list = request.session.get('rbac_menu_permission_session_key').get('rbac_menu_key')
    permission_list = request.session.get('rbac_menu_permission_session_key').get('rbac_menu_permission_key')
    all_menu_dict = {}
    for row in all_menu_list:
        row['child'] = []  # 添加孩子
        row['status'] = False  # 是否显示菜单
        row['opened'] = False  # 是否默认打开
        all_menu_dict[row['id']] = row  # 创建成字典形式

    # 权限列表，
    """
    {'permission__menu_id': None, 'permission__url': '/app02/wenjian.html', 'permission__caption': '上传文件'}，
    权限'permission__menu_id'：None即不挂靠在菜单列表下，如上传头像，但url下有
    """
    for per in permission_list:
        if not per['permission__menu_id']:
            continue
        item = {
            'id': per['permission__id'],
            'caption': per['permission__caption'],
            'parent_id': per['permission__menu_id'],
            'url': per['permission__url'],
            'status': True,  # 是否显示菜单
            'opened': False,  # 是否默认打开
        }
        # 只有访问的url地址与权限下的url地址一致时，opened=True,即访问会打开该链接的菜单列表
        if re.match(per['permission__url'],request.path_info):
        # if re.match(per['permission__url'], "/app02/order.html"):
            item['opened'] = True

        # 把权限列表添加到菜单字典child下,关联关系item['parent_id'] = all_menu_dict[id]
        pid = item['parent_id']
        all_menu_dict[pid]['child'].append(item)

        # 将当前权限前辈status=True
        temp = pid  # 父亲ID
        while not all_menu_dict[temp]['status']:  # 父级的的['status']为假才进行设置
            all_menu_dict[temp]['status'] = True  # 把当前父级设置为True即可见
            temp = all_menu_dict[temp]['parent_id']  # 循环上一父级，进行设置，直到最后的父级['parent_id'] = None
            if not temp:
                break
        # 将当前权限前辈opened=True
        if item['opened']:
            temp1 = pid  # 父亲ID
            while not all_menu_dict[temp1]['opened']:
                all_menu_dict[temp1]['opened'] = True
                temp1 = all_menu_dict[temp1]['parent_id']
                if not temp1:
                    break

        ###########处理菜单和菜单之间的等级关系################

    result = []
    for row in all_menu_list:
        pid = row['parent_id']
        if pid:
            all_menu_dict[pid]['child'].append(row)
        else:
            result.append(row)
    # ###########结构化处理结果################
    # for row in result:
        # print('--?',row)

    return result


def build_menu_tree_html(menu_list):

    tpl1 = """
     <div class='menu-item'>
         <div class='menu-header'>{0}</div>
         <div class='menu-body {2}'>{1}</div>
     </div>
     """
    tpl2 = """
     <a href='{0}' class='{1}'>{2}</a>
     """
    menu_str = ""
    for menu in menu_list:
        if not menu['status']:
            continue
        # menu：菜单，权限（url）
        if menu.get('url'):
            # 权限
            menu_str += tpl2.format(menu['url'], 'active' if menu['opened'] else '', menu['caption'])
        else:
            # 菜单
            if menu['child']:
                child_html = build_menu_tree_html(menu['child'])
            else:
                child_html = ''
            menu_str += tpl1.format(menu['caption'], child_html, '' if menu['opened'] else 'hide')
    return menu_str

@register.simple_tag
def rbac_menu(request):
    """
    根据session中当前用户的菜单信息以及当前url生成菜单
    :param request: 请求对象
    :return:
    """
    menu_tree_list = process_menu_tree_data(request)

    return mark_safe(build_menu_tree_html(menu_tree_list))



@register.simple_tag
def rbac_css():
    file_path = os.path.join('rbac','theme',settings.RBAC_THEME,'rbac.css')
    print('---file',file_path)
    #路径是否存在
    if os.path.exists(file_path):
        return mark_safe(open(file_path,'r',encoding='utf-8').read())
    else:
        raise Exception('rbac主题css文件不存在 ')

@register.simple_tag
def rbac_js():
    file_path = os.path.join('rbac','theme',settings.RBAC_THEME,'rbac.js')
    #路径是否存在
    if os.path.exists(file_path):
        return mark_safe(open(file_path,'r',encoding='utf-8').read())
    else:
        raise Exception('rbac主题JavaScript文件不存在 ')