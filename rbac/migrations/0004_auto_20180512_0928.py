# Generated by Django 2.0.3 on 2018-05-12 01:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0007_auto_20180512_0928'),
        ('rbac', '0003_auto_20180510_1918'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='menu',
            name='parent',
        ),
        migrations.RemoveField(
            model_name='permission',
            name='menu',
        ),
        migrations.AlterUniqueTogether(
            name='permission2action2role',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='permission2action2role',
            name='action',
        ),
        migrations.RemoveField(
            model_name='permission2action2role',
            name='permission',
        ),
        migrations.RemoveField(
            model_name='permission2action2role',
            name='role',
        ),
        migrations.RemoveField(
            model_name='user2role',
            name='role',
        ),
        migrations.RemoveField(
            model_name='user2role',
            name='user',
        ),
        migrations.DeleteModel(
            name='Action',
        ),
        migrations.DeleteModel(
            name='Menu',
        ),
        migrations.DeleteModel(
            name='Permission',
        ),
        migrations.DeleteModel(
            name='Permission2Action2Role',
        ),
        migrations.DeleteModel(
            name='Role',
        ),
        migrations.DeleteModel(
            name='User',
        ),
        migrations.DeleteModel(
            name='User2Role',
        ),
    ]
