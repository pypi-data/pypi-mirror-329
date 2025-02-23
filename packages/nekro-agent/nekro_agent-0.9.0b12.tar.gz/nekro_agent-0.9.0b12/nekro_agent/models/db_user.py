from tortoise import fields
from tortoise.models import Model


class DBUser(Model):
    """数据库用户模型"""

    id = fields.IntField(pk=True, generated=True, description="用户ID")
    username = fields.CharField(max_length=128, description="用户名")
    password = fields.CharField(max_length=128, description="密码")
    bind_qq = fields.CharField(max_length=32, unique=True, description="绑定的QQ号")

    perm_level = fields.IntField(description="权限等级")
    login_time = fields.DatetimeField(description="上次登录时间")

    # prevent_trigger_until = fields.IntField(description="禁止触发截止时间", default=0)
    # prevent_interact_until = fields.IntField(description="禁止互动截止时间", default=0)

    create_time = fields.DatetimeField(auto_now_add=True, description="创建时间")
    update_time = fields.DatetimeField(auto_now=True, description="更新时间")

    @property
    def is_active(self) -> bool:
        """用户是否激活"""
        return True  # 默认所有用户都是激活状态

    class Meta:
        table = "user"
