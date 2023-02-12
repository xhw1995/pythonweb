from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from kaka_mall import settings
"""
TimedJSONWebSignatureSerializer：可以对数据进行加密，设置有效时间
参数
    secret_key：秘钥
    expire_in=None：数据有效时间，单位-秒
    
注意：该类在2.0以上版本中被删除
解决方法：
    1 降低版本
    2 使用authlib库
"""
def generic_email_verify_token(user_id):
    # 1 创建实例
    s = Serializer(secret_key=settings.SECRET_KEY, expires_in=3600*24)
    # 2 加密数据
    data = s.dumps({'user_id':user_id})
    # 3 返回数据
    return data