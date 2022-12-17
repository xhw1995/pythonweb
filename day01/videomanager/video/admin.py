from django.contrib import admin

# Register your models here.
from video.models import VideoInfo,PeopleInfo

# 注册视频模型
admin.site.register(VideoInfo)
# 注册人物模型
admin.site.register(PeopleInfo)