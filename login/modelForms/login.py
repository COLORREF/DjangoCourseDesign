from django import forms
from login import models
from login.utils.bootstrapForms import BootstrapModelForm
from login.utils.md5 import md5


class LoginForm(BootstrapModelForm):
    captcha = forms.CharField(label="验证码", widget=forms.TextInput, required=True)

    class Meta:
        model = models.Admin
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_name'].widget.attrs['placeholder'] = '请输入管理员用户名'
        self.fields['user_name'].required = True
        self.fields['password'].widget = forms.PasswordInput(
            render_value=True,  # 禁止查看明文密码
            attrs={'class': 'form-control', 'placeholder': '请输入密码'})
        self.fields['password'].required = True
        self.fields['captcha'].widget.attrs['placeholder'] = '请输入验证码'

    def clean_password(self):
        return md5(self.cleaned_data['password'])  # 对密码进行md5加密

    def clean(self):
        """登录时不用验证用户名唯一性"""
        self._validate_unique = False
        return self.cleaned_data
