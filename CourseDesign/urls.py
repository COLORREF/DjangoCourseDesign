from django.contrib import admin
from django.urls import path
from login.views import login
from login.views import backstageManagement


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login.login),
    path('login/', login.login),
    path('login_check/', login.loginCheck),
    path('captcha_interface/', login.captcha_interface),
    path('backstage_management/', backstageManagement.backstage_management),
]
