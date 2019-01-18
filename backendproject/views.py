import json
from builtins import int

from django.http import JsonResponse
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password
from .serializers import *
from .models import *
from rest_framework import generics
from django.contrib import auth
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from datetime import date
from django.db.models import Sum
from backendproject import models
from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Q


# Create your views here.

class ProjectList(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def get_queryset(self):
        department_id = self.request.GET.get('department_id')
        department = Department.objects.filter(id=department_id)[0]
        self.queryset = Project.objects.filter(department_id=department)
        return self.queryset


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
        project.save()
        serializer = ProjectInfoSerializer(project)
        return Response(serializer.data)


class DepartmentListForAdvance(APIView):

    def get(self, request):
        department = []
        for item in Department.objects.all():
            department.append(
                {'department_id': item.id, 'department_name': item.name})
        return JsonResponse(department, safe=False)


class Login(APIView):
    def post(self, request):
        receive = request.data
        username = receive['userName']
        password = receive['password']
        user = auth.authenticate(username=username, password=password)
        if user:
            return Response({'id': user.id, 'token': 'admin'},
                            status=status.HTTP_200_OK)
        return Response(data={'token': 'admin'})

    def get(self, request):
        ACCESS = [
            'project_staff',
            'super_admin',
            'finance',
            'department_manager',
            'admin']
        id = request.GET.get('id')
        user = User.objects.get(id=id)
        data = {
            'name': user.profile.name,
            'user_id': user.id,
            'department_id': user.profile.department_id,
            'access': ACCESS[user.profile.access],
            'token': ACCESS[user.profile.access]
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
        self.queryset = Department.objects.filter(id=department_id)[
            0].user_profile
        return self.queryset


class DepartmentList(APIView):
    # 所有表项的部门外键List(可用于下拉框）

    def get(self, request):
        department = []
        for item in Department.objects.all():
            department.append(
                {'department_id': item.id, 'department_name': item.name})
        return JsonResponse(department, safe=False)


class ProjectListAll(APIView):
    # 所有表项的项目下拉
    def get(self, request):
        project = []
        for item in Project.objects.all():
            project.append(
                {'project_id': item.id, 'project_title': item.title})
        return JsonResponse(project, safe=False)


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
        end_time = date(
            year=start_time.year + 3,
            month=start_time.month,
            day=start_time.day)
        income = project.project_income.filter(
            time__range=(start_time, end_time))
        income_list = []

        for item in income:
            income_list.append({
                'date': str(item.time)[0:7],
                'number': item.confirm_num
            })
        expend_list = []
        expend = project.project_confirm.filter(
            time__range=(start_time, end_time))
        for item in expend:
            expend_list.append({
                'date': str(item.time)[0:7],
                'number': item.number
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
        if begin_time and end_time:
            project = Project.objects.filter(id=id)[0]
            income = project.project_income.filter(
                time__range=(begin_time[:10], end_time[:10])).values('category').annotate(
                value=Sum('confirm_num'))
            expend = project.project_confirm.filter(time__range=(
                begin_time[:10], end_time[:10])).values('category').annotate(value=Sum('number'))
        else:
            project = Project.objects.filter(id=id)[0]
            income = project.project_income.values(
                'category').annotate(value=Sum('confirm_num'))
            expend = project.project_confirm.values(
                'category').annotate(value=Sum('number'))
        return Response({'income': income, 'expend': expend},
                        status=status.HTTP_200_OK)


class ConfirmExpendListForExpend(APIView):

    def get(self, request):
        project_id = self.request.GET.get('project_id')
        project = Project.objects.filter(id=project_id)[0]
        confirm_expend = []
        for item in ConfirmExpend.objects.filter(project=project):
            confirm_expend.append({'confirm_expend_id': item.id, 'confirm_expend_category': item.category,
                                   'confirm_expend_title': item.title})
            print(item.title)
        return JsonResponse(confirm_expend, safe=False)


class ListAdvanceInfo(APIView):

    def get(self, request):
        advance = []
        for item in Advance.objects.all():
            advance.append({
                'department_id': item.project.department.id,
                'department_name': item.project.department.name,
                'project_id': item.project.id,
                'project_title': item.project.title,
                'receivable_title': item.title,
                'advance_num': item.number})
        return JsonResponse(advance, safe=False)


class ListConfirmExpendInfo(APIView):

    def get(self, request):
        confirm_expend = []
        for item in ConfirmExpend.objects.all():
            confirm_expend.append({
                'department_id': item.project.department.id,
                'department_name': item.project.department.name,
                'project_id': item.project.id,
                'project_title': item.project.title,
                'confirm_expend_id': item.id,
                'confirm_expend_category': item.category,
                'confirm_expend_title': item.title,
                'confirm_expend_num': item.number
            })
        return JsonResponse(confirm_expend, safe=False)


class ListIncomeInfo(APIView):

    def get(self, request):
        income = []
        for item in Income.objects.all():
            income.append({
                'department_id': item.project.department.id,
                'department_name': item.project.department.name,
                'project_id': item.project.id,
                'project_title': item.project.title,
                'income_id': item.id,
                'receivable_title': item.title,
                'receivable_category': item.category,
                'confirm_num': item.confirm_num,
                'tax_rate': item.tax_rate
            })
        return JsonResponse(income, safe=False)


class ListUser(APIView):
    # 列出全部人员（用于项目管理员添加项目人员）
    def get(self, request):
        list = []
        for item in UserProfile.objects.filter(license=1):
            list.append({'user_id': item.id,
                         'name': item.name,
                         'email': item.email,
                         'department_id2': item.department.id})
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
                id = data.project_id  # 前端选择一个project传进来
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
        receive = request.data
        request_id = receive['request_id']
        content = receive['content']
        whether = receive['whether']
        staff_request = StaffRequest.objects.filter(id=request_id)[0]
        staff = staff_request.staff
        project = staff_request.project
        if whether == 'true':
            project.out_staff.add(staff)
            staff_request.whether = 1
        else:
            staff_request.whether = -1
            staff_request.content = content
        staff_request.save()
        return Response(staff_request.whether, status=status.HTTP_200_OK)

    def get(self, request):
        department_id = request.GET.get('department_id')
        UserRequestSerializer(
            StaffRequest.objects.filter(
                department=department_id),
            many=True)
        return Response(
            UserRequestSerializer(
                StaffRequest.objects.filter(
                    department=department_id),
                many=True).data,
            status=status.HTTP_200_OK)


class ListUserRequest(APIView):
    # 列出部门人员请求的列表

    def get(self, request):
        project_id = request.GET.get('project_id')
        department_id = request.GET.get('department_id')
        if project_id:
            out_staff = StaffRequest.objects.filter(project_id=project_id)
            return UserRequestSerializer(out_staff, many=True)
        out_staff = StaffRequest.objects.filter(department=department_id)
        return UserRequestSerializer(out_staff, many=True)


class AddFinancialModel(APIView):
    # 给项目添加编辑财务模型

    def get(self, request):
        data = request.GET.getlist('data[]')
        project_id = request.GET.get('project_id')
        for item in data:
            item = json.loads(item)
            if item['status'] != 0:
                id = item['id']
                if id != 0:
                    model = FinancialModel(
                        id=item['id'],
                        project_id=project_id,
                        status=item['status'], name=item['name'],
                        number=item['number'])
                    model.save()
                else:
                    model = FinancialModel(
                        project_id=project_id,
                        status=item['status'], name=item['name'],
                        number=item['number'])
                    model.save()
        return Response({'info': 'success'})


class CheckReceivableList(APIView):
    # 查看应收表

    def get(self, request):
        # project_id = self.request.GET.get('project_id')
        # project = Project.objects.filter(project_id=project_id)
        expend = []
        for item in Receivable.objects.all():
            expend.append(
                {
                    'expend_id': item.id,
                    'title': item.title,
                    'number': item.number,
                    'project_id': item.project.id,
                    'project_name': item.project.title,
                    'category_id': item.category.id,
                    'category_name': item.category.name,
                    'department_name': item.project.department.name

                }
            )
        return JsonResponse(expend, safe=False)


class ListProjectById(APIView):
    # project下拉
    #
    def get(self, request):
        userid = self.request.GET.get('user_id')
        print(self.request.GET)
        user = User.objects.filter(id=userid)[0]
        project = user.staff_project.all()
        project_1 = []
        for item in project:
            project_1.append(
                {'project_id': item.id, 'project_name': item.title})
        return JsonResponse(project_1, safe=False)


class ListAddReceivable(APIView):
    # 添加应收表类别下拉
    def get(self, request):
        project_id = self.request.GET.get('project_id')
        project = Project.objects.filter(id=project_id)[0]
        category = []
        for item in FinancialModel.objects.filter(project=project, status=1):
            category.append(
                {'category_id': item.id, 'category_name': item.name})
        return JsonResponse(category, safe=False)


class ListAddExpend(APIView):
    # 添加费用表类别下拉
    def get(self, request):
        project_id = self.request.GET.get('project_id')
        project = Project.objects.filter(id=project_id)[0]
        category = []
        for item in FinancialModel.objects.filter(project=project, status=2):
            print()
            category.append(
                {'category_id': item.id, 'category_name': item.name})
        return JsonResponse(category, safe=False)


class ListCategoryForExpend(APIView):
    # 费用类别表下拉
    def get(self, request):
        project_id = self.request.GET.get('project_id')
        project = Project.objects.filter(id=project_id)[0]
        category = []
        for item in Expend.objects.filter(project=project):
            category.append({'category_id': item.category.id,
                             'category_name': item.category.name})
        return JsonResponse(category, safe=False)


class ListCategoryForReceivable(APIView):
    # 应收类别表下拉
    def get(self, request):
        project_id = self.request.GET.get('project_id')
        project = Project.objects.filter(id=project_id)[0]
        category = []
        for item in Receivable.objects.filter(project=project):
            category.append({'category_id': item.category.id,
                             'category_name': item.category.name})
        return JsonResponse(category, safe=False)


class CheckExpend(APIView):
    # 查看费用表
    def get(self, request):
        # project_id = self.request.GET.get('project_id')
        # project = Project.objects.filter(project_id=project_id)
        expend = []
        for item in Expend.objects.all():
            expend.append(
                {
                    'expend_id': item.id,
                    'title': item.title,
                    'number': item.number,
                    'project_id': item.project.id,
                    'project_name': item.project.title,
                    'category_id': item.category.id,
                    'category_name': item.category.name,
                    'department_name': item.project.department.name

                }
            )
            return JsonResponse(expend, safe=False)


class AddReceivable(APIView):

    # 应收表的插入
    def post(self, request):
        project_id = self.request.POST.get('project_id')
        print(request.POST.get)
        project = Project.objects.filter(id=project_id)[0]
        category_id = self.request.POST.get('category_id')
        category = FinancialModel.objects.filter(id=category_id)[0]
        title = self.request.POST.get('title')
        number = self.request.POST.get('number')
        agreement = self.request.FILES.get('agreement')
        Receivable.objects.create(
            project=project,
            category=category,
            title=title,
            number=number,
            agreement=agreement
        )
        return JsonResponse({'info': 'success'})


class AddExpend(APIView):
    # 费用表的插入
    def post(self, request):
        project_id = self.request.POST.get('project_id')
        project = Project.objects.filter(id=project_id)[0]
        category_id = self.request.POST.get('category')
        category = FinancialModel.objects.filter(id=category_id)[0]
        title = self.request.POST.get('title')
        number = self.request.POST.get('number')
        agreement = self.request.FILES.get('agreement2')
        print(agreement)
        Expend.objects.create(
            project=project,
            category=category,
            title=title,
            number=number,
            agreement=agreement
        )
        return JsonResponse({'info': 'success'})


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


class SendEmail(APIView):
    def get(self, request):
        BASE_URL = 'http://localhost:8080/register'
        email = request.GET.get('email')
        department_id = request.GET.get('department_id')
        if email and department_id:
            user = User.objects.create_user(username=email)
            UserProfile.objects.create(
                user=user, email=email, department_id=department_id)
            url_id = '?department_id=' + \
                     department_id + '&user=' + str(user.id)
            msg = '<a href=\"' + BASE_URL + url_id + '\">点击激活</a>'
            print(msg)
            send_mail(
                '标题',
                '内容',
                settings.EMAIL_FROM,
                [email],
                html_message=msg)
        return Response(status=status.HTTP_200_OK)


class Register(APIView):
    def post(self, request):
        receive = request.data
        print(receive)
        user_id = receive['user']
        username = receive['username']
        password = receive['password']
        name = receive['name']
        user = User.objects.filter(id=user_id)[0]
        user.username = username
        user.password = make_password(password)
        user.save()
        user_profile = user.profile
        user_profile.name = name
        user_profile.save()
        return Response(data=user.password, status=status.HTTP_200_OK)


class ReceivableListForAdvance(APIView):

    def get(self, request):
        project_id = self.request.GET.get('project_id')
        project = Project.objects.filter(id=project_id)[0]
        receivable = []
        result = []
        for item in Receivable.objects.filter(project=project):
            receivable.append({'receivable_category': item.category.name})
        for item in receivable:
            if item not in result:
                result.append(item)
        return JsonResponse(result, safe=False)


class ReceivableListForIncome(APIView):

    def get(self, request):
        project_id = self.request.GET.get('project_id')
        project = Project.objects.filter(id=project_id)[0]
        receivable = []
        r = []
        for item in Receivable.objects.filter(project=project):
            receivable.append({'receivable_category': item.category.name})
        for item in receivable:
            if item not in r:
                r.append(item)
        return JsonResponse(r, safe=False)


class UseCategoryGetReceivable(APIView):

    def get(self, request):
        receivable_category = self.request.GET.get('receivable_category')
        fm = FinancialModel.objects.filter(name=receivable_category)[0]
        receivable = []
        for item in Receivable.objects.filter(category=fm, advance_state='0', income_state='0'):
            receivable.append({'receivable_id': item.id, 'receivable_title': item.title})
        return JsonResponse(receivable, safe=False)


class UseCategoryGetReceivableForIncome(APIView):

    def get(self, request):
        receivable_category = self.request.GET.get('receivable_category')
        print(receivable_category)
        fm = FinancialModel.objects.filter(name=receivable_category)[0]
        print(fm)
        receivable = []
        for item in Receivable.objects.filter(category=fm, income_state='0'):
            receivable.append({'receivable_id': item.id, 'receivable_title': item.title})
        print(receivable)
        return JsonResponse(receivable, safe=False)


class AdvanceTitleList(APIView):

    def get(self, request):
        project_id = self.request.GET.get('project_id')
        project = Project.objects.filter(id=project_id)[0]
        advance = []
        for item in Advance.objects.filter(project=project):
            advance.append({
                'advance_id': item.id,
                'advance_title': item.title
            })
        return JsonResponse(advance, safe=False)


class IncomeTitleList(APIView):

    def get(self, request):
        project_id = self.request.GET.get('project_id')
        project = Project.objects.filter(id=project_id)[0]
        income = []
        for item in Income.objects.filter(project=project):
            income.append({
                'income_id': item.id,
                'income_title': item.title
            })
        return JsonResponse(income, safe=False)


class ExpendListForExpend(APIView):

    def get(self, request):
        project_id = self.request.GET.get('project_id')
        project = Project.objects.filter(id=project_id)[0]
        expend = []
        for item in Expend.objects.filter(project=project):
            expend.append({
                'expend_id': item.id,
                'expend_category': item.category.name,
                'expend_title': item.title
            })
        return JsonResponse(expend, safe=False)


class HandleConfirmExpend(APIView):

    def post(self, request):
        project_id = self.request.POST.get('project_id')
        project = Project.objects.filter(id=project_id)[0]
        confirm_expend_title = self.request.POST.get('confirm_expend_title')
        print(confirm_expend_title)
        expend = Expend.objects.filter(title=confirm_expend_title)[0]
        category = expend.category.name
        confirm_expend_num = self.request.POST.get('confirm_expend_num')
        expend_agreement = self.request.FILES.get('expend_agreement')
        models.ConfirmExpend.objects.create(
            project=project,
            category=category,
            title=confirm_expend_title,
            number=confirm_expend_num,
            agreement=expend_agreement)
        return JsonResponse({'info': 'success'})


class RecordAdvance(APIView):

    def post(self, request):
        project_id = self.request.POST.get('project_id')
        project = Project.objects.filter(id=project_id)[0]
        category = self.request.POST.get('receivable_category')
        fm = FinancialModel.objects.filter(name=category)[0]
        receivable_title = self.request.POST.get('receivable_title')
        advance_number = self.request.POST.get('advance_number')
        advance_number = int(advance_number)
        advance_agreement = self.request.FILES.get('advance_agreement')
        Advance.objects.create(
            project=project,
            category=category,
            title=receivable_title,
            number=advance_number,
            agreement=advance_agreement)
        r = Receivable.objects.filter(title=receivable_title, category=fm)[0]
        r.advance_state = 1
        r.save()
        return JsonResponse({'info': 'success'})


class ConfirmIncome(APIView):

    def post(self, request):
        print(request.POST)
        project_id = self.request.POST.get('project_id')
        project = Project.objects.filter(id=project_id)[0]
        receivable_category = self.request.POST.get('receivable_category')
        fm = FinancialModel.objects.filter(name=receivable_category)[0]
        receivable_title = self.request.POST.get('receivable_title')
        confirm_num = self.request.POST.get('confirm_num')
        confirm_num = int(confirm_num)
        tax_rate = self.request.POST.get('tax_rate')
        tax_rate = float(tax_rate)
        income_agreement = self.request.FILES.get('income_agreement')
        Income.objects.create(
            project=project,
            category=receivable_category,
            title=receivable_title,
            confirm_num=confirm_num,
            tax_rate=tax_rate,
            agreement=income_agreement)
        r = Receivable.objects.filter(title=receivable_title, category=fm)[0]
        r.income_state = 1
        r.save()
        print(receivable_category)
        print(receivable_title)
        return JsonResponse({'info': 'success'})


class AllStaffs(APIView):
    def get(self, request):
        project_id = request.GET.get('project_id')
        department_id = Project.objects.get(id=project_id).department_id
        all_staff = []
        for item in UserProfile.objects.filter(department_id=department_id, access=0):
            name = "未命名"
            if item.name:
                name = item.name
            all_staff.append({
                'key': item.user.id,
                'name': name
            })
        staff = ProjectStaffSerializer(
            Project.objects.filter(
                id=project_id)[0]).data
        data = {'all_staff': all_staff, 'project_staff': staff['staff']}
        return Response(data)


class OutStaffList(APIView):
    def get(self, request):
        project_id = request.GET.get('project_id')
        project = Project.objects.filter(id=project_id)[0]
        department_id = project.department_id
        all_staff = []
        for item in UserProfile.objects.filter(~Q(department_id=department_id), access=0):
            name = "未命名"
            if item.name:
                name = item.name
            all_staff.append({
                'key': item.user.id,
                'name': name
            })
        staff = ProjectOutStaffSerializer(
            Project.objects.filter(
                id=project_id)[0]).data
        data = {'all_staff': all_staff, 'project_staff': staff['staff']}
        return Response(data)


class ChangeStaff(APIView):
    def post(self, request):
        receive = request.data
        project_id = receive['project_id']
        direction = receive['direction']
        move_keys = receive['moveKeys'].split(',')
        project = Project.objects.filter(id=project_id)[0]
        user = User.objects.filter(id__in=move_keys)
        if direction == 'left':
            for item in user:
                project.staff.remove(item)
        else:
            for item in user:
                project.staff.add(item)
        return Response(ProjectInfoSerializer(project).data)


class ChangeOtherStaff(APIView):
    def post(self, request):
        receive = request.data
        project_id = receive['project_id']
        direction = receive['direction']
        move_keys = receive['moveKeys'].split(',')
        project = Project.objects.filter(id=project_id)[0]
        user = User.objects.filter(id__in=move_keys)
        if direction == 'left':
            for item in user:
                project.out_staff.remove(item)
        else:
            for item in user:
                project.out_staff.add(item)
        return Response(ProjectInfoSerializer(project).data)


class UserRequest(APIView):
    def post(self, request):
        receive = request.data
        request_id = receive['request_id']
        content = receive['content']
        whether = receive['whether']
        staff_request = StaffRequest.objects.filter(id=request_id)[0]
        staff = staff_request.staff
        project = staff_request.project
        if whether == 'true':
            project.staff.add(staff)
            staff_request.whether = 1
        else:
            staff_request.whether = -1
            staff_request.content = content
        staff_request.save()
        return Response(staff_request.whether, status=status.HTTP_200_OK)

    def get(self, request):
        department_id = request.GET.get('department_id')
        UserRequestSerializer(
            StaffRequest.objects.filter(
                department=department_id),
            many=True)
        return Response(
            UserRequestSerializer(
                StaffRequest.objects.filter(
                    department=department_id),
                many=True).data,
            status=status.HTTP_200_OK)


class CloseProject(APIView):
    def get(self, request):
        project_id = request.GET.get('project_id')
        project = Project.objects.filter(id=project_id)[0]
        project.status = 0
        project.save()
        return Response(status=status.HTTP_200_OK)


class GetFinancialModel(APIView):
    # 给项目添加编辑财务模型
    def get(self, request):
        project_id = request.GET.get('project_id')
        model = FinancialModel.objects.filter(project_id=project_id)
        data = FinancialModelSerializer(model, many=True).data
        return Response(data)


class AddProject(APIView):

    def post(self, request):
        receive = request.data
        project = Project.objects.create(title=receive['title'],
                                         leader_id=receive['leader'],
                                         begin_time=receive['begin_time'][:10],
                                         end_time=receive['end_time'][:10],
                                         content=receive['content'],
                                         department_id=receive['department_id']
                                         )
        return Response(ProjectSerializer(project).data)


class AddNewDepartment(APIView):

    def post(self, request):
        department_name = self.request.POST.get('department_name')
        try:
            User.objects.create_user(username=department_name, password=department_name)
            user = User.objects.filter(username=department_name)[0]
            department = Department.objects.create(name=department_name, leader=user)
            UserProfile.objects.create(access=3, department=department, user=user, name=user.username)
            return JsonResponse({'info': 'success'})
        except:
            return JsonResponse({'info': 'failed'})


class AddLeaderToNewDepartment(APIView):

    def post(self, request):
        department_name = self.request.POST.get('department_name')
        username = self.request.POST.get('username')
        name = self.request.POST.get('name')
        email = self.request.POST.get('email')
        phone = self.request.POST.get('phone')
        sex = self.request.POST.get('sex')
        try:
            department = Department.objects.filter(name=department_name)[0]
            department.leader = User.objects.create_user(username=username, password=username)
            new_user = User.objects.filter(username=username)[0]
            UserProfile.objects.create(user=new_user, name=name, email=email, access=3, phone=phone, gender=sex)
            department.save()
            return JsonResponse({'info': 'success'})
        except:
            return JsonResponse({'info': 'failed'})


class AddFinancialStaff(APIView):

    def post(self, request):
        username = self.request.POST.get('username')
        name = self.request.POST.get('name')
        email = self.request.POST.get('email')
        phone = self.request.POST.get('phone')
        sex = self.request.POST.get('sex')
        try:
            User.objects.create_user(username=username, password=username)
            new_user = User.objects.filter(username=username)[0]
            UserProfile.objects.create(user=new_user, name=name, email=email, access=2, phone=phone, gender=sex)
            return JsonResponse({'info': 'success'})
        except:
            return JsonResponse({'info': 'failed'})
