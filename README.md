1. ����rbac APP���µ���Ŀ�� ����Ҫ��settings��ע��
2. ���ݿ�Ǩ��
    1. �û���ļ̳�
        class User(models.Model):
        """
        �û���
        """

        roles = models.ManyToManyField(Role, verbose_name='�û���ӵ�еĽ�ɫ', blank=True) #Role�����ַ�������ʽ  ����ķ�ʽ

        class Meta:
            abstract = True   # ��ǰ�ı��������ݿ������ɣ�������Ϊ���࣬������̳�
    2. �����rbac��migrations�ĳ���__init__֮�������py�ļ�
    3. ִ�����ݿ�Ǩ�Ƶ�����

3. rbac��·������
        url(r'rbac/', include('rbac.urls',namespace='rbac')),
4. Ȩ����Ϣ��¼��
    ¼���ɫ
    ¼��һ���˵�
    ¼��Ȩ����Ϣ
        ��������  ע�⣺ ���е�urlҪ��name
    Ȩ�޵ķ���
        ע��  ʹ����ȷ���û���
        ����ɫ����Ȩ��
        ���û������ɫ


5. Ӧ�����м��
    ��settins��ע���м��
    MIDDLEWARE = [
                ...
                'rbac.middlewares.rbac.RbacMiddleWare',
            ]

    ��settins�м���Ȩ�޵��������
6. ��¼�ɹ�����ȫ����Ϣ�ĳ�ʼ��
    from rbac.service.permission import init_permission
    ��½�ɹ���
        init_permission(request,obj)

7. Ӧ�ö����˵�
    {% load rbac %}
    {% menu request %}

    Ӧ��css js
       <link rel="stylesheet" href="{% static 'rbac/css/menu.css' %} "/>
       <script src="{% static 'rbac/js/menu.js' %} "></script>

8. ·������
    {% breadcrumb request %}


9. Ȩ�����ȿ��Ƶ���ť����
    {% load rbac %}
    {% if request|has_permission:'class_add' %}
        <a class="btn btn-success btn-sm" style="margin: 3px" href="{% url 'class_add' %}"> <i
                class="fa fa-plus-square"></i> ��� </a>
    {% endif %}
