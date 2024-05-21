from django import forms
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from backstageManagement import models


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = models.Employee
        # fields = ['name',
        #           'age',
        #           'gender',
        #           'password',
        #           'account',
        #           'create_time',
        #           'department']
        fields = "__all__"
        # exclude = ['account']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {'class': 'form-control'}
        self.fields['account'].widget.attrs = {'step': '0.01', 'class': 'form-control'}


def employee_management(request):
    all_user_info: QuerySet = models.Employee.objects.all()
    # for info in all_user_info:
    #     print(
    #         info.id,
    #         info.name,
    #         info.age,
    #         info.password,
    #         info.account,
    #         info.create_time.strftime("%Y-%m-%d"),  # 年月日时间
    #         info.department.industry_title,  # 部门名称
    #         info.get_gender_display()  # 性别get_字段名_display
    #     )
    form = EmployeeForm()
    return render(request, '员工管理.html', {'all_user_info': all_user_info, 'form': form})


def add_employee(request):
    if request.method == "POST":
        form = EmployeeForm(data=request.POST)
        if form.is_valid():  # 校验数据
            # print(form.cleaned_data)  # 获取提交的所有信息key:value形式
            form.save()  # 提交保存进数据库
            return redirect('/员工管理')
        else:
            # print(form.errors)  # 打印错误信息
            return render(request, '添加员工.html', {"form": form})
    elif request.method == "GET":
        form = EmployeeForm()
        return render(request, '添加员工.html', {"form": form})


def delete_employee(request):
    employee_id = request.GET.get('employee_id')
    try:
        models.Employee.objects.filter(id=employee_id).delete()
    except Exception as e:
        print(e)
    return redirect('/员工管理/')


def edit_employee(request, employee_id):
    edit_data = models.Employee.objects.filter(id=employee_id).first()  # 根据id获取要编辑的数据

    if request.method == "GET":
        form = EmployeeForm(instance=edit_data)  # 根据修改前的实例构造form
        return render(request, '编辑员工.html', {'form': form})

    elif request.method == "POST":
        form = EmployeeForm(data=request.POST, instance=edit_data)  # 需要修改的是原来的实例，设定instance值
        # 如果不设置instance,那么save是新建数据
        if form.is_valid():  # 校验数据
            form.save()  # 合法直接修改保存
            return redirect('/员工管理/')  # 重定向回管理页面
        return render(request, '编辑员工.html', {'form': form})
