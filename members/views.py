from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework import response, status, permissions, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Task, TaskInvite
from .serializers import TaskSerializer, TaskInviteSerializer

class TaskListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve all tasks created by the authenticated user",
        responses={200: TaskSerializer(many=True)}
    )
    def get(self, request):
        tasks = Task.objects.filter(created_by=request.user)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Create a new task",
        request_body=TaskSerializer,
        responses={201: TaskSerializer, 400: "Bad Request"},
    )
    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskInviteView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Create a new task invite",
        request_body=TaskInviteSerializer,
        responses={201: TaskInviteSerializer, 400: "Bad Request"},
    )
    def post(self, request):
        serializer = TaskInviteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(invited_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Update an invite status (Accept/Decline)",
        manual_parameters=[
            openapi.Parameter("invite_id", openapi.IN_PATH, description="Invite ID", type=openapi.TYPE_INTEGER),
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={"status": openapi.Schema(type=openapi.TYPE_STRING, example="accepted")},
        ),
        responses={200: TaskInviteSerializer, 404: "Not Found"},
    )
    def patch(self, request, invite_id):
        try:
            invite = TaskInvite.objects.get(id=invite_id, invitee=request.user)
        except TaskInvite.DoesNotExist:
            return Response({"error": "Invite not found"}, status=status.HTTP_404_NOT_FOUND)

        invite.status = request.data.get("status", invite.status)
        invite.save()
        return Response(TaskInviteSerializer(invite).data)

    @swagger_auto_schema(
        operation_description="Get all invites for the authenticated user",
        responses={200: TaskInviteSerializer(many=True)}
    )
    def get(self, request):
        invites = TaskInvite.objects.filter(invitee=request.user)
        serializer = TaskInviteSerializer(invites, many=True)
        return Response(serializer.data)

