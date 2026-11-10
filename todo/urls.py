from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token # 作业6 登录token接口

urlpatterns = [
    # 作业7 注册
    path('register/', views.register, name="register"),
    # 作业6 登录获取token
    path('login/', obtain_auth_token, name="login"),
    # 作业3 列表+新增
    path('todos/', views.TodoListCreate.as_view(), name="todo-list-create"),
    # 作业4 详情/修改/删除
    path('todos/<int:pk>/', views.TodoRetrieveUpdateDestroy.as_view(), name="todo-detail"),
    # 作业8 标记完成切换
    path('todos/<int:pk>/toggle/', views.TodoToggleComplete.as_view(), name="todo-toggle"),
]
