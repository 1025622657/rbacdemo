
class RbacView(object):
    def dispatch(self,request,*args,**kwargs):
        permission_code = request.permission_code.lower()#当前用户权限操作
        handler = getattr(self,permission_code)
        return handler(request,*args,**kwargs)