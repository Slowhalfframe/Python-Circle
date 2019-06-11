# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-02-26 08:08
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('q_title', models.CharField(max_length=256, verbose_name='问题标题')),
                ('q_miaoshu', models.TextField(verbose_name='问题描述')),
                ('q_create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('q_change_time', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('q_link_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='关联用户')),
            ],
        ),
        migrations.CreateModel(
            name='Question_count',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('browse_num', models.IntegerField(default=0, verbose_name='被浏览量')),
                ('question', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='question.Question', verbose_name='关联问题')),
            ],
        ),
        migrations.CreateModel(
            name='Question_Type',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=150, unique=True, verbose_name='问题类别名称')),
                ('cover', models.ImageField(default='/static/type_cover/default.jpg', upload_to='static/question/type_cover', verbose_name='问题类配图')),
                ('intro', models.TextField(verbose_name='问题类别描述')),
            ],
        ),
        migrations.AddField(
            model_name='question',
            name='q_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='question.Question_Type', verbose_name='问题分类'),
        ),
        migrations.AddField(
            model_name='question',
            name='user_more_info',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.User_more_info', verbose_name='关联用户更多信息'),
        ),
    ]