from django.db import models


class Menu(models.Model):
    title = models.CharField("菜单名", max_length=32)
    icon = models.CharField("图标", max_length=32)
    wight = models.IntegerField(default=1, verbose_name="权重")  # 权重

    def __str__(self):
        return self.title


class Permission(models.Model):
    url = models.CharField("权限", max_length=108)
    name = models.CharField("URL别名", max_length=108)
    title = models.CharField("权限名字", max_length=32)
    menu = models.ForeignKey("Menu", null=True, blank=True)
    parent = models.ForeignKey('Permission', null=True, blank=True)

    def __str__(self):
        return self.title


class Role(models.Model):
    name = models.CharField("角色名字", max_length=32)
    permissions = models.ManyToManyField("Permission", verbose_name="角色的所有权限", blank=True)

    def __str__(self):
        return self.name


class User (models.Model):
    # name = models.CharField("用户名", max_length=32)
    # pwd = models.CharField("密码", max_length=32)
    roles = models.ManyToManyField(Role, verbose_name="用户所有的角色", blank=True)

    class Meta:
        abstract = True







