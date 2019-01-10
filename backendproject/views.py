from django.http import JsonResponse
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.hashers import make_password
from rest_framework.authtoken.models import Token
from .serializers import *
from .models import *
from rest_framework import generics
from django.contrib import auth
from rest_framework.response import Response
from rest_framework import status


# Create your views here.

class ProjectList(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def get_queryset(self):
        department_id = self.request.GET.get('department_id')
        department = Department.objects.filter(id=department_id)[0]
        self.queryset = Project.objects.filter(department_id=department)
        return self.queryset


class Login(APIView):
    def post(self, request):
        receive = request.data
        username = receive['username']
        password = receive['password']
        print(username)

        user = auth.authenticate(username=username, password=password)
        if user:

            # Token.objects.filter(user=user).delete()
            # auth.login(request, user)
            # data = {
            #     'id': user.id,
            #     'name': user.profile.name,
            #     'access': user.profile.access,
            #     'department': user.profile.department.id,
            #     'token': 'super_admin',
            # }
            serializer = UserSerializer(user)
            print(user)
            Token.objects.filter(user=user).delete()
            token = Token.objects.create(user=user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return JsonResponse({'result': 0, 'message': '登录失败'})

