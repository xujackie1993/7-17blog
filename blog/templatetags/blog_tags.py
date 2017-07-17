# coding:utf-8
from ..models import Post, Category, Tag
from django import template
from django.db.models.aggregates import Count

# 它还只是一个纯 Python 函数，Django 在模板中还不知道该如何使用它。为了能够通过 {% get_recent_posts %} 的语法
# 在模板中调用这个函数，必须按照 Django 的规定注册这个函数为模板标签
register = template.Library()


@register.simple_tag
def get_recent_posts(num=5):
    return Post.objects.all().order_by('-created_time')[:num]


@register.simple_tag
def archives():
    return Post.objects.dates('created_time', 'month', order='DESC')


@register.simple_tag
def get_categories():
    # 记得在顶部引入 count 函数
    # Count 计算分类下的文章数，其接受的参数为需要计数的模型的名称
    return Category.objects.annotate(
        num_posts=Count('post')).filter(
        num_posts__gt=0)


@register.simple_tag
def get_tags():
    # 记得在顶部引入 Tag model
    return Tag.objects.annotate(
        num_posts=Count('post')).filter(
        num_posts__gt=0)
