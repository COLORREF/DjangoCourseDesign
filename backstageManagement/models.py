from django.db import models


class Department(models.Model):
    """部门表"""
    industry_title = models.CharField(verbose_name="部门名称", max_length=32)

    def __str__(self):
        return self.industry_title


class Employee(models.Model):
    """员工表"""
    name = models.CharField(verbose_name="姓名", max_length=32)
    age = models.IntegerField(verbose_name="年龄")

    gender_choices = (
        (1, "男"),
        (2, "女"),
    )
    gender = models.SmallIntegerField(verbose_name="性别", choices=gender_choices)

    password = models.CharField(verbose_name="密码", max_length=32)
    account = models.DecimalField(verbose_name="余额", max_digits=10, decimal_places=2, default=0)

    # create_time = models.DateTimeField(verbose_name="入职时间", auto_now_add=False)
    create_time = models.DateField(verbose_name="入职时间", auto_now_add=False)

    # on_delete=models.CASCADE 级联删除
    # models.SET_NULL 删除置空
    department = models.ForeignKey(verbose_name="部门名称",
                                   to="Department",
                                   to_field="id",
                                   on_delete=models.CASCADE)