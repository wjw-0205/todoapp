from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import TodoSerializer
from todo.models import Todo

from django.db import IntegrityError
from django.contrib.auth.models import User
from rest_framework.parsers import JSONParser
from rest_framework.authtoken.models import Token
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


# 作业7 注册接口
@csrf_exempt
def register(request):
    if request.method == "POST":
        data = JSONParser().parse(request)
        try:
            # create_user 自动加密密码，重点！
            user = User.objects.create_user(username=data["username"], password=data["password"])
            token = Token.objects.create(user=user)
            return JsonResponse({"token": token.key, "username": user.username})
        except IntegrityError:
            return JsonResponse({"error": "用户名已存在"}, status=400)
    return JsonResponse({"error": "仅支持POST请求"}, status=400)


# 作业3 列表查询 + 创建新todo
class TodoListCreate(generics.ListCreateAPIView):
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Todo.objects.filter(user=user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# 作业4 单条：获取详情 / 修改 / 删除
class TodoRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Todo.objects.filter(user=user)


# 作业8 标记完成切换（修复400报错版本，APIView，允许空PATCH）
class TodoToggleComplete(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk, user):
        return Todo.objects.get(pk=pk, user=user)

    def patch(self, request, pk):
        todo = self.get_object(pk, request.user)
        todo.completed = not todo.completed
        todo.save()
        return Response(TodoSerializer(todo).data)