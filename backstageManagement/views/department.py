from django import forms
from django.db.models.query import QuerySet
from django.http import JsonResponse
from django.shortcuts import render

from backstageManagement import models


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = models.Department
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {'class': 'form-control'}


def divisional_management(request):
    """部门管理页面"""
    departments: QuerySet = models.Department.objects.all()  # 获取所有部门信息
    form = DepartmentForm()
    return render(request, "部门管理.html", {'departments': departments, 'form': form})


def add_divisional(request):
    """添加部门"""
    form = DepartmentForm(request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse({'status': True})

    return JsonResponse({'status': False, 'error': form.errors})


def delete_divisional(request):
    """删除部门"""
    uid = request.POST["uid"]
    if models.Department.objects.filter(id=uid).exists():
        models.Department.objects.filter(id=uid).delete()
        return JsonResponse({'status': True})
    return JsonResponse({'status': False, 'error': "删除失败，数据不存在"})


def edit_divisional(request):
    """修改部门"""
    uid = request.POST["uid"]
    new_name = request.POST["newName"]
    if models.Department.objects.filter(id=uid).exists():
        models.Department.objects.filter(id=uid).update(industry_title=new_name)
        return JsonResponse({'status': True})
    return JsonResponse({'status': False, 'error': "修改失败，数据不存在"})
