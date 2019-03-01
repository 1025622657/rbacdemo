
from django.forms import Form
from django.forms import fields
from django.forms import widgets
from web import models
from bs4 import BeautifulSoup

class addOrderForm(Form):
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
    create_user_id = fields.CharField(
        widget=widgets.CheckboxInput(attrs={"checked":"checked"})
    )

    status = fields.ChoiceField(
        choices=models.Order.status_choice,
        widget=widgets.Select(attrs={'class': 'form-control'})
    )







