from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from login import models
from login.modelForms.login import LoginForm
from login.utils.captcha import base64_captcha
from login.utils.errorDict import errorDict


def login(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, '登录.html', {'form': form})


def loginCheck(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)

        # 表单没有空字段
        if form.is_valid():
            captcha = form.cleaned_data.pop('captcha')  # 用户输入的验证码
            session_captcha = request.session.get('captcha')  # 从session表中获取的验证码
            cookie_captcha = request.COOKIES.get('captcha', '')  # 从cookie中获取验证码

            # 验证码失效（已使用过）
            if session_captcha is None:
                print("验证码失效")
                errors = errorDict(form=form, fields_errors={"captcha": "验证码已失效"})
                return JsonResponse({'errors': errors, 'captcha': 'failure'}, status=400)  # 返回包含错误信息的 JSON 数据

            # 验证码超时
            if not session_captcha or not cookie_captcha:
                print("验证码超时")
                errors = errorDict(form=form, fields_errors={"captcha": "验证码超时,请点击验证码刷新"})
                return JsonResponse({'errors': errors, 'captcha': 'timeout'}, status=400)

            # 验证码正确
            if captcha.upper() == session_captcha.upper() == cookie_captcha.upper():
                print("验证码正确")
                request.session.pop('captcha')  # 从session表中删除的验证码，使验证码失效
                try:
                    admin = models.Admin.objects.get(user_name=form.cleaned_data['user_name'])  # 根据用户名查找管理员数据

                # 查找失败抛出异常，表示用户不存在
                except models.Admin.DoesNotExist:
                    print("用户不存在")
                    errors = errorDict(form=form, fields_errors={"password": "用户名或密码错误"})
                    return JsonResponse({'errors': errors}, status=401)

                # 用户存在但密码错误
                if form.cleaned_data['password'] != admin.password:
                    print("用户存在但密码错误")
                    errors = errorDict(form=form, fields_errors={"password": "用户名或密码错误"})
                    return JsonResponse({'errors': errors}, status=401)

                # 用户名和密码都正确
                else:
                    print("登录成功")
                    # return redirect('/backstage_management/', permanent=True)  # 重定向到后台管理页面
                    # 因为Ajax和CORS限制，不能直接使用redirect进行重定向
                    return JsonResponse({'redirect': 'backstage_management/'})  # 直接返回重定向的url

            # 验证码错误
            else:
                print("验证码错误")
                errors = errorDict(form=form, fields_errors={"captcha": "验证码错误"})
                return JsonResponse({'errors': errors, 'captcha': 'error'}, status=403)

        # 表单有空字段
        else:
            # 后端校验
            print("表单有空字段")
            return JsonResponse({'errors': errorDict(form)}, status=400)


def captcha_interface(request):
    # 生成验证码
    base64_str, code_str = base64_captcha()

    # 后端session设置验证码校验存储
    request.session['captcha'] = code_str
    request.session.set_expiry(60)  # 60秒超时

    # 前端设置验证码校验存储
    response = HttpResponse(base64_str)
    response.set_cookie('captcha', code_str, max_age=60)  # 设置验证码 Cookie，并设置60秒超时
    return response
