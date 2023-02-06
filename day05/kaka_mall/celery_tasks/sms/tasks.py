# 生产者 -- 任务，函数

"""
1 函数 必须让celery的实例的 task装饰器装饰
2 需要celery 自动检测指定包的任务（详见main.py）
"""
from libs.yuntongxun.sms import CCP
from celery_tasks.main import app

# 让celery的实例的 task装饰器装饰
@app.task
def celery_send_sms_code(mobile, code):
    """
    参数
        to：手机号
        [code, expire]：短信验证码，有效期
        temp_id：模板编号
    """
    CCP.send_template_sms(mobile, [code, 5], 1)