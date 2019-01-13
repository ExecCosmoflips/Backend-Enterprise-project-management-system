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
from django.http import Http404
from datetime import date
from django.db.models import Sum


# Create your views here.

class ProjectList(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def get_queryset(self):
        department_id = self.request.GET.get('department_id')
        department = Department.objects.filter(id=department_id)[0]
        self.queryset = Project.objects.filter(department_id=department)
        return self.queryset

    def post(self, request, *args, **kwargs):
        receive = request.data
        print(receive['department_id'])
        Project.objects.create()


class ProjectInfo(APIView):
    def get_object(self, pk):
        try:
            return Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        id = request.GET.get('id')
        project = self.get_object(pk=id)
        serializer = ProjectInfoSerializer(project)
        return Response(serializer.data)

    def post(self, request):
        receive = request.data
        leader = User.objects.filter(id=receive['leader'])[0]
        project = Project.objects.filter(id=receive['id'])[0]
        project.leader = leader
        project.title = receive['title']
        project.content = receive['content']
        project.begin_time = receive['begin_time'][0:10]
        project.end_time = receive['end_time'][0:10]
        print(project.leader)
        project.save()
        serializer = ProjectInfoSerializer(project)
        return Response(serializer.data)


class Login(APIView):
    def post(self, request):
        receive = request.data
        username = receive['userName']
        password = receive['password']
        print(username)

        user = auth.authenticate(username=username, password=password)
        if user:
            serializer = UserSerializer(user)
            print(user)
            Token.objects.filter(user=user).delete()
            token = Token.objects.create(user=user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(data={'token': 'super_admin'})

    def get(self, request):
        data = {
            'name': 'super_admin',
            'user_id': '1',
            'access': ['super_admin', 'admin'],
            'token': 'super_admin',
            'avator': 'https://file.iviewui.com/dist/a0e88e83800f138b94d2414621bd9704.png'
        }
        return Response(data=data)


class PersonnelInfo(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        project_id = self.request.GET.get('project_id')
        self.queryset = Project.objects.filter(id=project_id)[0].personnel
        return self.queryset


class DepartmentStaff(generics.ListCreateAPIView):
    # 列出部门人员列表
    queryset = User.objects.all()
    serializer_class = UserInfoSerializer

    def get_queryset(self):
        department_id = self.request.GET.get('department_id')
        self.queryset = Department.objects.filter(id=department_id)[0].userprofile
        return self.queryset


class DepartmentList(APIView):
    # 所有表项的部门外键List(可用于下拉框）

    def get(self, request):
        department = []
        for item in Department.objects.all():
            department.append({'department_id': item.id, 'department_name': item.name})
        return JsonResponse(department, safe=False)


class ProjectListAll(APIView):
    # 所有表项的项目下拉
    def get(self, request):
        project = []
        for item in Project.objects.all():
            project.append({'project_id': item.id, 'project_title': item.title})
        return JsonResponse(project, safe=False)


class getAddDepartmentAdmin(APIView):

    def post(self, request):
        department = self.request.POST.get('department')
        username = self.request.POST.get('username')
        name = self.request.POST.get('name')
        email = self.request.POST.get('email')
        gender = self.request.POST.get('gender')
        phone = self.request.POST.get('phone')

        Receivable.objects.create(
            department=department,
            username=username,
            name=name,
            email=email,
            gender=gender,
            phone=phone)
        return JsonResponse({'info': 'success'})


class GetAddTreasurer(APIView):
    def post(self, request):
        username = self.request.POST.get('username')
        name = self.request.POST.get('name')
        email = self.request.POST.get('email')
        gender = self.request.POST.get('gender')
        phone = self.request.POST.get('phone')

        Receivable.objects.create(
            username=username,
            name=name,
            email=email,
            gender=gender,
            phone=phone)
        return JsonResponse({'info': 'success'})


class SetupDepartmentName(APIView):
    def post(self, request):
        name = self.request.POST.get('name')

        Receivable.objects.create(
            name=name)
        return JsonResponse({'info': 'success'})


class GetProjectBarData(APIView):

    def get(self, request):
        id = request.GET.get('project_id')
        project = Project.objects.filter(id=id)[0]
        start_time = project.begin_time
        end_time = date(year=start_time.year + 3, month=start_time.month, day=start_time.day)
        income = project.project_income.filter(time__range=(start_time, end_time))
        income_list = []
        for item in income:
            income_list.append({
                'date': item.time,
                'number': item.confirm_num
            })
        expend_list = []
        expend = project.project_confirm.filter(time__range=(start_time, end_time))
        for item in expend:
            expend_list.append({
                'date': item.time,
                'number': item.confirm_num
            })
        data = {
            'expendList': expend_list,
            'incomeList': income_list
        }
        return Response(data, status=status.HTTP_200_OK)


class GetProjectPieData(APIView):

    def get(self, request):
        id = request.GET.get('project_id')
        begin_time = request.GET.get('begin_time')
        end_time = request.GET.get('end_time')
        project = Project.objects.filter(id=id)[0]
        data = project.project_income.filter(
            time__range=(begin_time, end_time)).values('category').annotate(value=Sum('confirm_num'))
        return Response(data, status=status.HTTP_200_OK)


class AddReceivable(APIView):

    # 应收表的插入

    def post(self, request):

        project_id = self.request.POST.get('project_id')
        project=Project.objects.filter(project_id=project_id)[0]
        category = self.request.POST.get('category')
        title = self.request.POST.get('title')
        number = self.request.POST.get('number')
        agreement = self.request.POST.get('agreement')
        Receivable.objects.create(
            project=project,
            category=category,
            title=title,
            number=number,
            agreement=agreement)
        return JsonResponse({'info': 'success'})


class ReceivableListForAdvance(APIView):
    # 收入表的收入类别下拉框（应收表的借用）
    def get(self, request):
        project_id = self.request.GET.get('project_id')
        project = Project.objects.filter(id=project_id)[0]
        receivable = []
        for item in Receivable.objects.filter(project=project):
            receivable.append({'receivable_id': item.id, 'receivable_title': item.title})
        return JsonResponse(receivable, safe=False)


class AddExpend(APIView):
    # 费用表的插入

    def post(self, request):
        project_id = self.request.POST.get('project_id')
        project = Project.objects.filter(project_id=project_id)[0]
        category = self.request.POST.get('category')
        title = self.request.POST.get('title')
        number = self.request.POST.get('number')
        agreement = self.request.POST.get('agreement')

        Expend.objects.create(
            project=project,
            category=category,
            title=title,
            number=number,
            agreement=agreement)
        return JsonResponse({'info': 'success'})


class AddAdvance(APIView):

    # 预收表的插入
    def post(self, request):
        project_id = self.request.POST.get('project_id')
        project = Project.objects.filter(project_id=project_id)[0]
        category = self.request.POST.get('category')
        number = self.request.POST.get('number')
        agreement = self.request.POST.get('agreement')
        Advance.objects.create(

            project=project,
            category=category,
            number=number,
            agreement=agreement)
        return JsonResponse({'info': 'success'})


class AddIncome(APIView):

    # 收入表的插入（确认收入功能）
    def post(self, request):
        project_id = self.request.POST.get('project_id')
        project = Project.objects.filter(project_id=project_id)[0]
        category = self.request.POST.get('category')  # 前端借用应收表的下拉框ReceivableListForAdvance方法
        confirm_num = self.request.POST.get('confirm_num')
        tax_rate = self.request.POST.get('tax_rate')
        agreement = self.request.POST.get('agreement')
        Income.objects.create(
            project=project,
            receivable=category,
            confirm_num=confirm_num,
            tax_rate=tax_rate,
            agreement=agreement)
        return JsonResponse({'info': 'success'})


class AddConfirmExpend(APIView):

    # 确认费用表的插入
    def post(self, request):
        project_id = self.request.POST.get('project_id')
        project = Project.objects.filter(project_id=project_id)[0]
        category = self.request.POST.get('category')
        number = self.request.POST.get('number')
        agreement = self.request.POST.get('agreement')
        ConfirmExpend.objects.create(
            project=project,
            category=category,
            number=number,
            agreement=agreement
        )
        return JsonResponse({'info': 'success'})


class ListUser(APIView):
    # 列出全部人员（用于项目管理员添加项目人员）
    def get(self, request):
        list = []
        for item in UserProfile.objects.filter(license=1):
            list.append({'user_id': item.id, 'name': item.name, 'email': item.email,'department_id2': item.department.id})
        return JsonResponse(list, safe=False)


class ListProjectInDepartment(APIView):
    # 列出本部门下的项目（用于应收表费用表下拉以及其他功能）
    def get(self, request):
        department_id = self.request.GET.get('department_id')
        department = Department.objects.filter(department_id=department_id)[0]
        list = []
        for item in Project.objects.filter(department=department):
            list.append({'project_id': item.id, 'project_title': item.title})
        return JsonResponse(list, safe=False)


class AddLocalDepartmentUser(APIView):
    # 添加本部门的成员信息
    def post(self, request):

        department_id = self.request.POST.get('department_id')
        department = Department.objects.filter(department_id=department_id)[0]
        name = self.request.POST.get('name')
        email = self.request.POST.get('email')
        phone = self.request.POST.get('phone')
        license = self.request.POST.get('license')

        UserProfile.objects.create(
                name=name,
                email=email,
                phone=phone,
                license=license,
                department=department
                 )
        return JsonResponse({'info': 'success'})


class AddUserRequest(APIView):
    # 发起添加项目人员请求
    def post(self, request):
        data = self.request.POST.get('data')
        for item in data:
            id = item.department_id
            department_id2 = UserProfile.department.filter(department_id=id)
            department_id = self.request.POST.get('department_id')
            if department_id != department_id2:
                staff = data.name
                id = data.project_id#前端选择一个project传进来
                project = Project.objects.filter(project_id=id)[0]
                StaffRequest.objects.create(
                    staff=staff,
                    project=project,

                )
            else:
                id = data.project_id
                staff = data.name
                Project.objects.filter(id=id).add(staff=staff)
        return JsonResponse({'info': 'success'})


class PastUserRequest(APIView):
    # 批准部门人员请求
    def post(self, request):
        whether_name = self.request.POST.get('whether')
        project_id=self.request.POST.get('project_id')
        project = Project.objects.filter(id=project_id)
        project_title = project.title
        staff = self.request.POST.get('staff')
        if whether_name == '批准':
            whether = 1
            Project.objects.filter(title=project_title).add(staff=staff)
        elif whether_name == '不批准':
            whether = 2
        StaffRequest.objects.update(
            whether=whether
        )

        return JsonResponse({'info': 'success'})




class ListUserRequest(generics.ListCreateAPIView):
    # 列出部门人员请求的列表

    queryset = StaffRequest.objects.all()
    serializer_class = ProjectSerializer

    def get_queryset(self):
        department_id = self.request.GET.get('department_id')
        department = Department.objects.filter(id=department_id)
        project = Project.objects.filter(department=department)
        self.queryset = StaffRequest.objects.filter(project=project)
        return self.queryset


class AddFinancialModel(APIView):
    # 给项目添加编辑财务模型
    def post(self, request):
        name = self.request.POST.get('name')
        number = self.request.POST.get('number')
        status_name = self.request.POST.get('status')
        if status_name == '费用类别':
            status = 0
            FinancialModel.objects.create(
                name=name,
                number=number,
                status=status
            )
        elif status_name == '收入类别':
            status = 1
            FinancialModel.objects.create(
                name=name,
                number=number,
                status=status
            )
        return JsonResponse({'info': 'success'})


class CheckReceivableList(APIView):
    # 查看应收表

    def get(self, request):
        project_id = self.request.GET.get('project_id')
        project=Project.objects.filter(project_id=project_id)
        receivable = []
        for item in Receivable.objects.filter(project=project):
            receivable.append(
                {'receivable_id': item.id, 'title': item.title, 'number': item.number, 'agreement': item.agreement})
        return JsonResponse(receivable, safe=False)




class CheckExpend(APIView):

    # 查看费用表

    def get(self, request):
        project_id = self.request.GET.get('project_id')
        project = Project.objects.filter(project_id=project_id)
        receivable = []
        for item in Expend.objects.filter(project=project):
            receivable.append(
                {'expend_id': item.id, 'title': item.title, 'number': item.number, 'agreement': item.agreement})
        return JsonResponse(receivable, safe=False)




class SetLogo(APIView):

    def post(self, request):
        logo = request.FILES.get('logo')
        company = Company.objects.create(logo=logo, name='company_name')
        return Response(company.logo.url, status=status.HTTP_200_OK)

    def get(self, request):
        data = Company.objects.last().logo
        return Response(data.url, status=status.HTTP_200_OK)


class ErrorLogger(APIView):

    def post(self, request):
        return Response(status=status.HTTP_200_OK)

    def get(self, request):
        return Response(status=status.HTTP_200_OK)
