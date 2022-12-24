from django.db import models

# Create your models here.
"""
1 模型类 需要继承自 models.Model
2 定义属性
    id 系统默认生成
    属性名 = models.类型(选项)
    
    2.1 属性名：字段名
        不要使用 python、MySQL关键字
        不要使用连续的下划线
    2.2 类型：MySQL的类型
    2.3 选项：是否有默认值，是否唯一，是否为null
        CharField 必须设置 max_length
        verbose_name 主要是 admin站点使用
3 改变表名称
    默认表的名称是：子应用名_类名（都是小写）
"""
class BookInfo(models.Model):
    # 创建字段，字段类型
    name = models.CharField(max_length=20, verbose_name="名称")
    pub_date = models.DateField(verbose_name="发布日期", null=True)
    readcount = models.IntegerField(default=0, verbose_name="阅读量")
    commentcount = models.IntegerField(default=0, verbose_name="评论量")
    is_delete = models.BooleanField(default=False, verbose_name="逻辑删除")

    #peopleinfo_set=[PeopleInfo, PeopleInfo, ...]    # 添加外键后，系统自动添加隐藏字段

    #peopleinfo

    class Meta:
        db_table = "bookinfo"   # 指明数据库表名
        verbose_name = "图书"    # 在admin站点中显示的名称

    def __str__(self):
        # 定义每个数据对象的显示信息
        return self.name


class PeopleInfo(models.Model):
    GENDER_CHOICES = (
        (1, 'male'),
        (2, 'female')
    )
    name = models.CharField(max_length=20, verbose_name="名称")
    gender = models.SmallIntegerField(choices=GENDER_CHOICES, default=1, verbose_name="性别")
    description = models.CharField(max_length=200, null=True, verbose_name="描述信息")
    """
    外键
    系统会自动为外键添加 _id
    
    外键的级联关系
    主表 和 从表
    1 对 多
    
    主表的一条数据 删除
    从表有关联数据时的操作？
        SET_NULL
        抛出异常，不让删除
        级联删除
        
    """
    book = models.ForeignKey(BookInfo, on_delete=models.CASCADE)    # 外键
    is_delete = models.BooleanField(default=False, verbose_name="逻辑删除")

    class Meta:
        db_table = "peopleinfo"
        verbose_name = "人物信息"

    def __str__(self):
        return self.name