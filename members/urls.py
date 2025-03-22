from django.urls import path
from .views import TaskListCreateView, TaskInviteView

urlpatterns = [
    path("tasks/", TaskListCreateView.as_view(), name="task-list-create"),
    path("invites/", TaskInviteView.as_view(), name="invite-list-create"),
    path("invites/<int:invite_id>/", TaskInviteView.as_view(), name="invite-update"),
]
