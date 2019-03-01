from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse
from rbacdemo import settings
import re
class RbacMiddleware(MiddlewareMixin):
    def process_request(self,request,*args,**kwargs):
        """
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        """{
            '/index.html': ["GET", "POST", "DEL", "Edit"],
            '/order.html': ["GET", "POST", "DEL", "Edit"],
            '/index-(\d+).html': ["GET", "POST", "DEL", "Edit"],
        }
        """
        """路过无需权限访问的URL"""
        for pattern in settings.RBAC_NO_AUTH_URL:
            if re.match(pattern,request.path_info):
                return None

        """获取当前用户session中的权限信息"""
        permission_dict = request.session.get(settings.RBAC_PERMISSION_SESSION_KEY)

        if not permission_dict:
            return HttpResponse(settings.RBAC_PERMISSION_MSG)

        """当前URL和session中的权限进行匹配"""
        flag = False
        for pattern,code_list in permission_dict.items():
            upper_code_list = [item.upper() for item in code_list ]

            #用户访问的url与他session中的权限匹配
            if re.match(pattern,request.path_info):
                # request.GET.get(settings.RBAC_QUERY_KEY,'GET'),即url没写?md=post时，默认为GET
                # request_permission_code = request.GET.get(settings.RBAC_QUERY_KEY,'GET').upper()
                request_permission_code = request.GET.get(settings.RBAC_QUERY_KEY, settings.RBAC_DEFAULT_QUERY_VALUE).upper()
                if request_permission_code in upper_code_list:
                    #当前权限信息
                    request.permission_code = request_permission_code
                    #当前url所有的权限信息,把方法处理成大写
                    request.permission_code_list = upper_code_list
                    flag = True
                    break
                    #存放在request.permission_code里，便于视图函数获取做相应操作
        if not flag:
            return HttpResponse(settings.RBAC_PERMISSION_MSG)


