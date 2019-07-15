1. 拷贝rbac APP到新的项目中 并且要在settings中注册
2. 数据库迁移
    1. 用户表的继承
        class User(models.Model):
        """
        用户表
        """

        roles = models.ManyToManyField(Role, verbose_name='用户所拥有的角色', blank=True) #Role不用字符串的形式  用类的方式

        class Meta:
            abstract = True   # 当前的表不会在数据库中生成，用于作为基类，让子类继承
    2. 清除掉rbac下migrations的除了__init__之外的所有py文件
    3. 执行数据库迁移的命令

3. rbac的路由配置
        url(r'rbac/', include('rbac.urls',namespace='rbac')),
4. 权限信息的录入
    录入角色
    录入一级菜单
    录入权限信息
        批量操作  注意： 所有的url要有name
    权限的分配
        注意  使用正确的用户表
        给角色分配权限
        给用户分配角色


5. 应用上中间件
    在settins中注册中间件
    MIDDLEWARE = [
                ...
                'rbac.middlewares.rbac.RbacMiddleWare',
            ]

    在settins中加上权限的相关配置
6. 登录成功进行全新信息的初始化
    from rbac.service.permission import init_permission
    登陆成功后
        init_permission(request,obj)

7. 应用二级菜单
    {% load rbac %}
    {% menu request %}

    应用css js
       <link rel="stylesheet" href="{% static 'rbac/css/menu.css' %} "/>
       <script src="{% static 'rbac/js/menu.js' %} "></script>

8. 路径导航
    {% breadcrumb request %}


9. 权限粒度控制到按钮级别
    {% load rbac %}
    {% if request|has_permission:'class_add' %}
        <a class="btn btn-success btn-sm" style="margin: 3px" href="{% url 'class_add' %}"> <i
                class="fa fa-plus-square"></i> 添加 </a>
    {% endif %}
