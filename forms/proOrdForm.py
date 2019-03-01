
from django.forms import Form
from django.forms import fields
from django.forms import widgets
from web import models
from bs4 import BeautifulSoup

class perOrderForm(Form):
    title = fields.CharField(max_length=10,
                             min_length=3,
                             error_messages={
                                 "required":'标题不能为空',
                                 "invaild":'格式为字符',
                                 "max_length":'最长10字符',
                                 "min_length":'最短3字符'
                             })
    detail = fields.CharField(
        widget=widgets.Textarea(attrs={'id': 'content'}),
             min_length=10,
             error_messages={
                 "required": '内容不能为空',
                 "invaild": '格式为字符',
                 "min_length": '最短10字符'
                             })
    # create_user_id = fields.CharField(
    #     widget=widgets.CheckboxInput(attrs={"checked":"checked"})
    # )
    create_user_id = fields.ChoiceField(
        widget=widgets.RadioSelect(attrs={'checked': 'checked'})
    )
    ctime = fields.DateTimeField(required=False)
    status = fields.ChoiceField(
        choices=models.Order.status_choice,
        widget=widgets.Select
    )

    processor_id = fields.CharField(
        widget=widgets.CheckboxInput
    )
    solution = fields.CharField(
        widget=widgets.Textarea(attrs={'id': 'content'}),
        required=False,
        min_length=5,
        error_messages={
            "required": '内容不能为空',
            "invaild": '格式为字符',
            "min_length": '最短5字符'
        }
    )
    ptime = fields.DateTimeField(required=False)
    def __init__(self, request, *args, **kwargs):
        super(perOrderForm, self).__init__(*args, **kwargs)
        self.request = request
        self.fields['create_user_id'].choices = ((1,self.request.session['user_info']['nickname']),)
        print("---------self",self.fields['create_user_id'].choices)







