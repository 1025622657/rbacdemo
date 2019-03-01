
from django.shortcuts import HttpResponse,render,redirect
from web import models
from forms.orderForm import addOrderForm
from forms.proOrdForm import perOrderForm
from django.views import View
from rbac.cbv.views import RbacView
from django.db.models import Q
import datetime
import time
import json
from django.db.models import Count
from django.db import connection,connections

def login(request):
    if request.method == "GET":
        return render(request,'login.html')
    else:
        u = request.POST.get('username')
        p = request.POST.get('password')
        obj = models.UserInfo.objects.filter(user__username=u,user__password=p).first()

        if obj:
            request.session['user_info'] = {
                "username":u,"nickname":obj.nickname,"nid":obj.id
            }
            #获取当前用户权限
            #获取当前用户菜单
            #去配置文件中获取key,写入session中
            from rbac.service import initial_permission
            initial_permission(request,obj.user_id)
            return redirect('/index.html')
        else:
            return render(request,'login.html')
def index(request):
    print("判断登录成功与否，则重定向index.html")
    if not request.session.get('user_info'):
        return redirect('/login.html')
    return render(request,'index1.html')


def trouble(request):
    if request.permission_code == "LOOK":
        trouble_list = models.Order.objects.filter(create_user_id=request.session['user_info']['nid'])
        return render(request,'trouble.html',{"trouble_list":trouble_list})

    elif request.permission_code == "DELETE":
        nid = request.GET.get('nid')
        models.Order.objects.filter(create_user_id=request.session['user_info']['nid'],id=nid).delete()
        return redirect('/trouble.html')

    elif request.permission_code == "POST":
        if request.method == "GET":
            createOrder = addOrderForm(initial={"status":1})
            return render(request,"trouble_add.html",{"createOrder":createOrder})
        else:
            createOrder = addOrderForm(request.POST)
            if createOrder.is_valid():
                create_order_info =createOrder.cleaned_data
                create_order_info['create_user_id'] = request.session.get('user_info').get('nid')
                import datetime
                # models.Order.objects.create(ctime=datetime.datetime.now(),title=title,detail=content,create_user_id=request.session['user_info']['nid'])
                models.Order.objects.create(**create_order_info)
                return redirect('/trouble.html')
            return render(request, "trouble_add.html", {"createOrder": createOrder})

    elif request.permission_code == "EDIT":
        if request.method == "GET":
            nid = request.GET.get('nid')
            s = models.Order.objects.filter(id=nid).values('title','detail','ctime','status').first()
            OrderObj = addOrderForm(initial=s)
            return render(request,"trouble_edit.html",{"OrderObj":OrderObj,"nid":nid})
        else:
            nid = request.GET.get('nid')
            title = request.POST.get('title')
            detail = request.POST.get('detail')
            status = request.POST.get('status')
            order_info = {
                "title":title,
                "detail":detail,
                "status":status,
                "create_user_id":request.session['user_info']['nid'],
            }
            models.Order.objects.filter(id=nid).update(**order_info)
            return redirect('/trouble.html')

    elif request.permission_code == "DETAIL":
        nid = request.GET.get("nid")
        detail_obj = models.Order.objects.filter(id=nid).first()
        time = models.Order.objects.filter(id=nid).extra(
        select={'ctime': "date_format(ctime,'%%Y-%%m-%%d')"}).values('ctime').first()
        return render(request,"trouble_detail.html",{"detail_obj":detail_obj,"time":time})


def trouble_kill(request):

    nid = request.session['user_info']['nid']
    order_id = request.GET.get('nid')

    if request.permission_code == "LOOK":
        #查看列表:未解决的(即未抢的)，当前用户已经解决的或正在解决，并按状态进行升序排序
        trouble_list = models.Order.objects.filter(Q(status=1)|Q(processor_id=nid)).order_by('status')
        return render(request,'trouble_kill_look.html',{"trouble_list":trouble_list})

    elif request.permission_code == "EDIT":
        if request.method == "GET":
            #已经抢到了，状态【处理中】未处理
            if models.Order.objects.filter(id=order_id,processor_id=nid,status=2):
                obj = models.Order.objects.filter(id=order_id).first()
                return render(request,'trouble_kill_edit.html',{"obj":obj})

            # 已经抢到了，状态【已处理】
            elif models.Order.objects.filter(id=order_id,processor_id=nid,status=3):
                return HttpResponse('已处理')

            #抢【未处理】状态的，没抢到，如果抢到v有返回值，同时状态置为【处理中】
            #同时点，数据库有锁，v表示受影响的行数，v为真时，表示抢成功
            v = models.Order.objects.filter(id=order_id,status=1).update(processor_id=nid,status=2)
            if not v:
                return HttpResponse('没抢到')
            else:
                obj = models.Order.objects.filter(id=order_id).first()
                return render(request,'trouble_kill_edit.html',{"obj":obj})
        else:

            order_id = request.GET.get('nid')
            solution = request.POST.get('solution')
            models.Order.objects.filter(id=order_id,processor_id=nid).update(status=3,solution=solution,ptime=datetime.datetime.now())
            return redirect('/trouble-kill.html')

    elif request.permission_code == "DETAIL":
        obj = models.Order.objects.filter(id=order_id, processor_id=nid).first()
        untreatedObj = models.Order.objects.filter(id=order_id, status=1).first()
        obj = obj if obj else untreatedObj
        return render(request,'trouble_kill_detail.html',{"obj":obj})



def report(request):
    if request.permission_code == "LOOK":
        if request.method == "GET":
            return render(request,'report.html')
        else:
            ymd_list = models.Order.objects.filter(status=3).extra(
                select={'ymd':'date_format(ptime,"%%Y-%%m-%%d")'}).values('processor_id','processor__nickname', 'ymd').annotate(
                ct=Count('id'))
            #折线型图表，查询所有【已处理】状态的订单，并按处理时间（年月日）进行分组(确定每个人每天的处理订单数量)
            #把数据处理成折线型图表的所需的数据结构
            ymd_dict = {}
            for row in ymd_list:
                #将字符串转化成时间戳，pchart图表只识别时间戳，且需转换数据float类型*1000
                row['ymd'] = time.mktime(time.strptime(row['ymd'], '%Y-%m-%d'))
                key = row['processor_id']
                if key in ymd_dict:
                    ymd_dict[key]['data'].append([float(row['ymd']) * 1000, row['ct']])
                else:
                    ymd_dict[key] = {'name': row['processor__nickname'], 'data': [[float(row['ymd']) * 1000, row['ct']], ]}
            #饼型图表
            #查询所有【已处理】状态的订单，并按处理人id进行分组(确定唯一性)，再把数据处理成图表所需的数据结构
            result_dic = {}
            result = models.Order.objects.filter(status=3).values('processor_id','processor__nickname').annotate(ct=Count('id'))
            for row in result:
                key = row['processor_id']
                if key not in result:
                    result_dic[key] = {"name":row['processor__nickname'],"y":row['ct']}

            #把图表所需数据传到前端
            response = {
                'pie':list(result_dic.values()),
                'line':list(ymd_dict.values()),
            }
            return HttpResponse(json.dumps(response))













