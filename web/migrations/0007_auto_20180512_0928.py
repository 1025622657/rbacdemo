# Generated by Django 2.0.3 on 2018-05-12 01:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0006_auto_20180511_1633'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='create_user',
        ),
        migrations.RemoveField(
            model_name='order',
            name='processor',
        ),
        migrations.RemoveField(
            model_name='userinfo',
            name='user',
        ),
        migrations.DeleteModel(
            name='Order',
        ),
        migrations.DeleteModel(
            name='UserInfo',
        ),
    ]