from django.urls import path
from .views import TaskListCreateView, InvitationCreateView, InvitationRespondView

urlpatterns = [
    path('tasks/', TaskListCreateView.as_view(), name='task-list-create'),
    path('invite/', InvitationCreateView.as_view(), name='invite-create'),
    path('invite/<int:id>/', InvitationRespondView.as_view(), name='invite-respond'),
]