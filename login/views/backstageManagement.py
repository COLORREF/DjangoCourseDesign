from django.shortcuts import render


def backstage_management(request):
    return render(request, '后台管理.html')
