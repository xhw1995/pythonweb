"""
生产者
    @app.task
    def celery_send_sms_code(mobile, code):
        CCP.send_template_sms(mobile, [code, 5], 1)

    app.autodiscover_tasks(['celery_tasks.sms'])

消费者
    celery -A proj worker -l INFO
    在虚拟环境下执行指令
    celery -A celery_tasks.main worker -l INFO

队列（中间人、经济人）
    设置broker：通过加载配置文件来设置
    app.config_from_object('celery_tasks.config')

    # 配置信息 key = value
    # 指定 redis为broker（中间人、经纪人、队列）
    broker_url = "redis://127.0.0.1:6379/15"

Celery -- 将3者实现
    为celery运行 设置Django环境
    import os
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kaka_mall.settings')

    创建celery实例
    from celery import Celery
    app = Celery(main='celery_tasks')
"""
# 1 为celery运行 设置Django环境
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kaka_mall.settings')

# 2 创建celery实例
from celery import Celery
"""
参数
    main：任务名称，设置脚本路径即可（因为脚本路径唯一）
"""
app = Celery(main='celery_tasks')

# 3 设置broker：通过加载配置文件来设置
app.config_from_object('celery_tasks.config')

# 4 celery 自动检测指定包的任务
"""
参数
    列表：列表元素是 tasks的路径
"""
app.autodiscover_tasks(['celery_tasks.sms', 'celery_tasks.email'])