# 运行依赖和说明

1、确保已安装Django，可以使用命令（需要设置环境变量）：`pip list`，查看运行结果中是否有Django
。若未安装，使用命令 `pip install Django` 安装，可以选择国内的镜像安装，清华大学镜像安装命令：
`pip install Django -i https://pypi.tuna.tsinghua.edu.cn/simple`

2、确保已安装PIL库，安装命令：`pip install pillow`,可以选择国内的镜像安装，清华大学镜像安装命令：
`pip install pillow -i https://pypi.tuna.tsinghua.edu.cn/simple`

3、请将 ...CourseDesign/login/utils/captcha.py文件中的 `font_path = 'D:/Desktop/CODE/Python/Django/CourseDesign/login/static/微软雅黑.ttf'`路径修改为自己电脑上的绝对路径
# 数据库说明

数据库使用是Django默认的SQLite文件数据库数据库，方便项目转移和共享。无需进行其他额外数据库操作。

只有一个管理员用户数据可用于登录，账号是：admin，密码是：123456，对应登录页面的账号和密码。
# 运行方式
运行方式1： 

- 使用PyCharm专业版打开该项目，添加Django运行配置，直接运行

运行方式2：

- 打开控制台并移动至manage.py同级目录下，运行命令（需要设置环境变量）：`python manage.py runserver 127.0.0.1:8000`
  `runserver`后面跟的是Django服务器运行的地址和端口，可自行修改

