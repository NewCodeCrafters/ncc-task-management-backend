from rest_framework import status
from rest_framework.response import Response
from rest_framework import response, status, permissions, views
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Task, Invitation
from .serializers import TaskSerializer, InvitationSerializer
from django.core.mail import send_mail
from django.conf import settings

class TaskListCreateView(APIView):
    @swagger_auto_schema(responses={200: TaskSerializer(many=True)})
    def get(self, request):
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)
    
    @swagger_auto_schema(request_body=TaskSerializer, responses={201: TaskSerializer})
    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class InvitationCreateView(APIView):
    @swagger_auto_schema(request_body=InvitationSerializer, responses={201: InvitationSerializer})
    def post(self, request):
        serializer = InvitationSerializer(data=request.data)
        if serializer.is_valid():
            invitation = serializer.save(invited_by=request.user)
            send_mail(
                subject=f"Invitation to join task: {invitation.task.title}",
                message=f"You have been invited to participate in the task '{invitation.task.title}'.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[invitation.email]
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class InvitationRespondView(APIView):
    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'status': openapi.Schema(type=openapi.TYPE_STRING, enum=['accepted', 'rejected'])
        }
    ), responses={200: "Invitation response updated", 400: "Invalid status", 404: "Invitation not found"})
    def patch(self, request, id):
        try:
            invitation = Invitation.objects.get(id=id)
        except Invitation.DoesNotExist:
            return Response({'error': 'Invitation not found'}, status=status.HTTP_404_NOT_FOUND)
        
        status_value = request.data.get('status')
        if status_value in ['accepted', 'rejected']:
            invitation.status = status_value
            invitation.save()
            return Response({'message': f'Invitation {status_value}'}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)
