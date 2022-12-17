from django.db import models

# Create your models here.
"""
1 模型类 需要继承自 models.Model
2 系统会自动添加一个主键 -- id
3 字段
    字段名 = model.类型(选项)
    字段名就是数据表的字段名
    字段不要使用 python/mysql等关键字
    
    char(M)、varchar(M)：M是选项
"""
class VideoInfo(models.Model):
    # 创建字段，字段类型...
    name = models.CharField(max_length=10)

    # 重写 str方法，让admin显示视频名称
    def __str__(self):
        """将模型类以字符串的方式输出"""
        return self.name

class PeopleInfo(models.Model):
    name = models.CharField(max_length=10)
    gender = models.BooleanField()
    # 外键约束：人物属于哪本书
    video = models.ForeignKey(VideoInfo,on_delete=models.CASCADE)


