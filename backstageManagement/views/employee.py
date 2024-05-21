from django import forms
from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe

from backstageManagement import models


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = models.Employee
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {'class': 'form-control'}
        self.fields['account'].widget.attrs = {'step': '0.01', 'class': 'form-control'}


def employee_management(request):

    # 搜索处理
    # all_info = models.PrettyNum.objects.all()  # .order_by("-level")  # order_by排序，-号从高到低，按级别排序
    data_dict = {}
    search_value = request.GET.get('search_value')
    if search_value:  # 如果不为为空
        data_dict['name__contains'] = search_value  # 字段名__contains 包含某个值

    # 根据页码计算出数据条数的起始位置和结束位置
    page = int(request.GET.get('page', '1'))  # 当前页
    page_size = 10  # 每一页的数据条数
    start_index = (page - 1) * page_size
    end_index = page * page_size

    # 添加页码标签

    # 计算页码，生成标签
    count = models.Employee.objects.filter(**data_dict).count()  # 数据总条数
    # 计算页码总数
    total_page_count, div = divmod(count, page_size)
    if div != 0:  # 如果有余数总页数要加1
        total_page_count += 1

    # 计算起始页码和结束页码为当前页的前后5页
    plus = 5
    if total_page_count <= 2 * plus + 1:  # 数据总量小于11（前后5页+选中1页）
        start_page = 1
        end_page = total_page_count + 1
    else:  # 数据量大于11
        if page <= plus:  # 当前选中的是前前5页，正常显示1-10页
            start_page = 1
            end_page = 2 * plus + 1
        else:  # 当前选中页大于5，显示前5页和后5页
            if (page + plus) > total_page_count:  # 如果选中的是最后几页，即当前选中页+5大于总页数
                start_page = total_page_count - 2 * plus  # 开始页为最后一页往前11个
                end_page = total_page_count + 1  # 最后页就是总页数
            else:
                start_page = page - plus
                end_page = page + plus + 1

    # 遍历生成页码
    page_str_list = []

    # 首页
    prev = '<li><a href="?page=1">首页</a></li>'
    page_str_list.append(prev)

    # 上一页
    if page > 1:
        prev = '<li><a href="?page={}">上一页</a></li>'.format(page - 1)
    else:
        prev = '<li><a href="#">上一页</a></li>'
    page_str_list.append(prev)

    for i in range(start_page, end_page):
        # 添加选中样式
        if i == page:
            label = '<li class="active"><a href="?page={}">{}</a></li>'.format(i, i)
        else:
            label = '<li><a href="?page={}">{}</a></li>'.format(i, i)
        page_str_list.append(label)

    # 下一页
    if page < total_page_count:
        prev = '<li><a href="?page={}">下一页</a></li>'.format(page + 1)
    else:
        prev = '<li><a href="#">下一页</a></li>'
    page_str_list.append(prev)

    # 尾页
    prev = '<li><a href="?page={}">尾页</a></li>'.format(total_page_count)
    page_str_list.append(prev)

    page_str = mark_safe("".join(page_str_list))

    all_user_info = models.Employee.objects.filter(**data_dict)[start_index:end_index]  # 取前十条数据

    form = EmployeeForm()
    return render(request,
                  '员工管理.html',
                  {"all_user_info": all_user_info, "form": form, "page_str": page_str})


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
