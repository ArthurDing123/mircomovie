# 微电影管理系统介绍

### 工具语言:
* 系统：deepin15.6(linux4.15内核 debian系列)
* 语言：python3.6
* 框架：Flask框架
* IDE: Pycharm

### 功能项目：
##### 后端功能：
* 登录、注册、退出、重置密码
* 标签管理、电影管理、预告管理、评论管理、收藏管理、日志管理、权限管理、角色管理、管理员管理
*  基本功能：各项管理的增删改查
##### 前端功能：
* 电影预告的轮训播图
* 根据　电影的**标签**、**星级**、**上映时间**、 **评论数**、**播放数**进行排序展示
* 会员中心的 修改密码、评论记录、登录日志、电影收藏列表
* 电影播放页面的电影播放功能、电影信息展示、电影评论列表

### 项目结构：

```
micromovie/
app/
        __init__.py   #初始化文件
        admin/          #后台蓝图
                    __init__.py
                    views.py  #后台路由
                    forms.py #后台表单
        home/                 #前台蓝图
                    __init__.py
                    views.py #前台路由
                    forms.py #前台表单
        static/　   #静态文件
                    uploads/　　#上传文件目录
        templates/
                    admin/ # 后台模板
                    home/  #前台模板
        models.py  #模型
config.py　　#通用配置文件
tools.py        #通用工具
run.py          #运行文件
```

### 使用的库:
```
alembic==0.9.9
blessings==1.6.1
bpython==0.17.1
certifi==2018.4.16
chardet==3.0.4
click==6.7
curtsies==0.3.0
defusedxml==0.5.0
dominate==2.3.1
Flask==1.0.2
Flask-Admin==1.5.1
Flask-Bootstrap==3.3.7.1
Flask-Login==0.4.1
Flask-Migrate==2.2.0
Flask-OpenID==1.2.5
Flask-Script==2.0.6
Flask-SQLAlchemy==2.3.2
Flask-WTF==0.14.2
greenlet==0.4.13
idna==2.7
itsdangerous==0.24
Jinja2==2.10
Mako==1.0.7
MarkupSafe==1.0
Pygments==2.2.0
PyMySQL==0.8.1
python-dateutil==2.7.3
python-editor==1.0.3
python3-openid==3.1.0
requests==2.19.1
six==1.11.0
SQLAlchemy==1.2.8
typing==3.6.4
urllib3==1.23
visitor==0.1.3
wcwidth==0.1.7
Werkzeug==0.14.1
WTForms==2.2.1

```
