"""
LoginRequiredMixin
    未登录用户 会返回 重定向
    重定向 并不是JSON数据

方法一 将LoginRequiredMixin类重写为LoginRequiredJSONMixin，让CenterView继承LoginRequiredJSONMixin
from django.contrib.auth.mixins import AccessMixin
class LoginRequiredJSONMixin(AccessMixin):
    # Verify that the current user is authenticated.

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # 此处修改为返回JSON数据
            return JsonResponse({'code': 400, 'errmsg': "用户尚未登录"})
        return super().dispatch(request, *args, **kwargs)

方法二 定义LoginRequiredJSONMixin类，继承LoginRequiredMixin。重写 handle_no_permission方法
"""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse

class LoginRequiredJSONMixin(LoginRequiredMixin):
    def handle_no_permission(self):
        return JsonResponse({'code': 400, 'errmsg': "用户尚未登录"})