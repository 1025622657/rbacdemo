from django.db import models
import datetime
from rbac.models import User as RbacUser

class UserInfo(models.Model):
    nickname = models.CharField(max_length=16)
    user = models.OneToOneField(RbacUser,on_delete=models.CASCADE)
    def __str__(self):
        return self.nickname

class Order(models.Model):
    """
    报障单
    """
    # nid = models.IntegerField(primary_key=True)
    # uid = models.UUIDField()#随机字符串

    title = models.CharField(verbose_name='标题',max_length=32)
    detail = models.TextField(verbose_name='详细')
    create_user = models.ForeignKey(UserInfo,related_name='cuser',on_delete=models.CASCADE)
    # ctime = models.FloatField() #时间戳
    # ctime = models.DateTimeField(auto_now_add=True,default=datetime.datetime.now)

    #不填则默认为当前时间，类似default=datetime.datetime.now
    ctime = models.DateTimeField(auto_now_add=True)
    # ctime = models.DateTimeField()
    status_choice = (
        (1,'未处理'),
        (2, '处理中'),
        (3, '已处理'),
    )
    status = models.IntegerField(choices=status_choice,default=1)
    processor = models.ForeignKey(UserInfo,related_name='puser',null=True,blank=True,on_delete=models.CASCADE)
    solution = models.TextField(null=True,blank=True)

    ptime = models.DateTimeField(null=True,blank=True)
    def __str__(self):
        return self.title
