"""
生产者 -- 任务，函数

1 函数 必须让celery的实例的 task装饰器装饰
2 需要celery 自动检测指定包的任务（详见main.py）
"""
from django.core.mail import send_mail
from celery_tasks.main import app

@app.task
def celery_send_email(subject, message, html_message, from_email, recipient_list):

    send_mail(subject=subject,
              message=message,
              html_message=html_message,
              from_email=from_email,
              recipient_list=recipient_list)