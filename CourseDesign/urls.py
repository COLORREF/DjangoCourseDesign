from django.contrib import admin
from django.urls import path
from login.views import login
from backstageManagement.views import department, employee

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', login.login),
    path('login/', login.login),
    path('login_check/', login.loginCheck),
    path('captcha_interface/', login.captcha_interface),
    path('logout/', login.logout),

    path('部门管理/', department.divisional_management),
    path('部门管理/添加部门/', department.add_divisional),
    path('部门管理/删除部门/', department.delete_divisional),
    path('部门管理/编辑部门/', department.edit_divisional),

    path('员工管理/', employee.employee_management),
    path('员工管理/添加员工/', employee.add_employee),
    path('员工管理/删除员工/', employee.delete_employee),
    path('员工管理/<int:employee_id>/编辑员工/', employee.edit_employee),
]
