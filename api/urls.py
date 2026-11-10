from django.urls import path
from .views import TodoListCreate, TodoRetrieveUpdateDestroy, TodoToggleComplete, SignupView, LoginView

urlpatterns = [
    path('todos/', TodoListCreate.as_view(), name='todo-list-create'),
    path('todos/<int:pk>/', TodoRetrieveUpdateDestroy.as_view(), name='todo-detail'),
    path('todos/<int:pk>/toggle/', TodoToggleComplete.as_view(), name='todo-toggle'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
]
