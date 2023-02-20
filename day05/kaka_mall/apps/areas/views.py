import json
import re

from django.core import cache
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render

# Create your views here.
from django.views import View

from utils.views import LoginRequiredJSONMixin

"""
需求
    获取省份信息
    
前端
    页面加载时，发送axios请求，获取省份信息    

后端
    请求：不需要请求参数
    业务逻辑：查询省份信息
    响应:JSON
    路由：areas/

步骤
    1 查询省份信息
    2 将对象转换为字典数据
    3 返回响应
"""
from areas.models import Area
class AreaView(View):
    def get(self, request):
        # 0 查询缓存数据
        province_list = cache.get('province')
        # 如果没有缓存数据，则查询数据库，并缓存数据
        if province_list is None:
            # 1 查询省份信息
            # 返回查询结果集，集中元素为对象
            provinces = Area.objects.filter(parent=None)
            # 2 将对象转换为字典数据
            province_list = []
            for province in provinces:
                province_list.append({
                    'id': province.id,
                    'name': province.name
                })
            # 2.1 保存缓存数据
            #cache.set(key, value, expire)
            cache.set('province', province_list, 3600*24)
        # 3 返回响应
        return JsonResponse({'code': 0, 'errmsg': "ok", 'province_list': province_list})


"""
需求
    获取市、区县信息

前端
    页面修改省、市时，发送axios请求，获取下一级信息    

后端
    请求：传递省id 或 市id
    业务逻辑：查询id查询信息，查询结果集转换为列表
    响应:JSON
    路由：areas/id

步骤
    1 查询省、市id，查询信息
    2 将对象转换为字典数据
    3 返回响应
"""
class SubAreaView(View):
    def get(self, request, id):
        # 0 查询缓存数据
        data_list = cache.get('city%s'%id)
        if data_list is None:
            # 1 查询省、市id，查询信息
            #Area.objects.filter(parent=id)
            #Area.objects.filter(parent_id=id)

            up_level = Area.objects.get(id=id)
            down_level = up_level.subs.all()
            # 2 将对象转换为字典数据
            data_list = []
            for item in down_level:
                data_list.append({
                    'id': item.id,
                    'name': item.name
                })
            # 2.1 保存缓存数据，默认保存在redis的default内
            cache.set('city:%s'%id, data_list, 24*3600)
        # 3 返回响应
        return JsonResponse({'code': 0, 'errmsg': "ok", 'sub_data': {'subs': data_list}})

"""
举例：商城项目
注册用户：1亿
日活用户：1%    1百万
下单比例：1%    1万
新增地址概率：1%    100    300次/天 
"""

# 不经常发生变化的数据，最好缓存到redis（内容）中，减少数据库的查询

"""
请求
业务逻辑（数据库的增删改查）
响应

增（注册）
    1 接收数据
    2 验证数据
    3 数据入库
    4 返回响应
删
    1 查询指定数据
    2 删除数据（物理删除，逻辑删除）
    3 返回响应
改（个人邮箱）
    1 查询指定数据
    2 接收数据
    3 验证数据
    4 数据更新
    5 返回响应
查（个人中心的数据展示，省市区）
    1 查询指定数据
    2 将对象数据转换为字典数据
    3 返回响应
"""

"""
需求
    新增地址
前端
    用户填写地址信息后，前端发送axios请求，会携带相关信息（POST--body）
后端
    请求：接受请求
    业务逻辑：数据入库
    响应：返回响应
    路由：POST    /addresses/create/
步骤
    1 接收数据
    2 获取参数，验证参数
    3 数据入库
    4 返回响应
"""
from users.models import Address
class AddressCreateView(LoginRequiredJSONMixin,View):
    def post(self, request):
        # 0 判断是否超过地址上限
        #Address.objects.filter(user=request.user).count()
        #count = request.user.addresses.count()
        #if count >= constans.USER_ADDRESS_COUNTS_LIMIT:
        #    return JsonResponse({'code': RETCODE.THROTTLINGERR, 'errmsg': "超过地址数量上限"})
        # 1 接收数据
        data = json.loads(request.body.decode())
        # 2 获取参数，验证参数
        receiver = data.get('receiver')
        province_id = data.get('province_id')
        city_id = data.get('city_id')
        district_id = data.get('district_id')
        place = data.get('place')
        mobile = data.get('mobile')
        tel = data.get('tel')
        email = data.get('email')

        user = request.user
        # 2.1 验证必传参数
        if not all([receiver, province_id, city_id, district_id, place, mobile]):
            return HttpResponseBadRequest("缺少必传参数")
        # 2.2 省市区id 是否正确

        # 2.3 详细地址长度

        # 2.4 手机号
        if not re.match(r'^1[3-9]\d{9}&', mobile):
            return HttpResponseBadRequest("手机号有误")
        # 2.5 固定电话
        if tel:
            if not re.match(r'^(0[0-9]{2,3}-)?([2-9][0-9]{6,7})+(-[0-9]{1,4})?$', tel):
                return HttpResponseBadRequest("固定电话有误")
        # 2.6 邮箱
        if email:
            if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
                return HttpResponseBadRequest("邮箱有误")

        # 3 数据入库
        address = Address.objects.create(
            user=user,
            title=receiver,
            receiver=receiver,
            province_id=province_id,
            city_id=city_id,
            district_id=district_id,
            place =place,
            mobile=mobile,
            tel=tel,
            email=email,
        )
        # 3.1 新增地址返回给前端，实现局部刷新
        address_dict = {
            "id": address.id,
            "title": address.title,
            "receiver": address.receiver,
            "province": address.province.name,
            "city": address.city.name,
            "district": address.district.name,
            "place": address.place,
            "mobile": address.mobile,
            "tel": address.tel,
            "email": address.email
        }

        # 4 返回响应
        return JsonResponse({'code': 0, 'errmsg': 'ok', 'address': address_dict})