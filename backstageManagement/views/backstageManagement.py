from django.shortcuts import render
from django.http import HttpResponse


def file_management(request):
    return render(request, '文件管理.html')


def write_off(request):
    return HttpResponse("")
