from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import TodoSerializer, TodoToggleCompleteSerializer
from todo.models import Todo
from django.db import IntegrityError
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


# 列表查询 + 创建新todo
class TodoListCreate(generics.ListCreateAPIView):
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Todo.objects.filter(user=user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# 单条：获取详情 / 修改 / 删除
class TodoRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Todo.objects.filter(user=user)


# 新增：切换任务完成状态视图
class TodoToggleComplete(generics.UpdateAPIView):
    serializer_class = TodoToggleCompleteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Todo.objects.filter(user=user)

    def perform_update(self, serializer):
        serializer.instance.completed = not serializer.instance.completed
        serializer.save()


# 用户注册接口（DRF APIView，自带浏览页面）
class SignupView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        try:
            username = request.data["username"]
            password = request.data["password"]
            user = User.objects.create_user(username=username, password=password)
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": str(token)}, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response({"error": "username taken. choose another username"}, status=status.HTTP_400_BAD_REQUEST)


# 用户登录接口（DRF APIView，自带浏览页面）
class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        try:
            username = request.data["username"]
            password = request.data["password"]
            user = User.objects.get(username=username)
            if user.check_password(password):
                token, created = Token.objects.get_or_create(user=user)
                return Response({"token": str(token)}, status=status.HTTP_200_OK)
            else:
                return Response({"error":"password wrong"}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"error":"user not found"}, status=status.HTTP_400_BAD_REQUEST)
