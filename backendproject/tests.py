# coding=utf-8
from django.test import TestCase
from backendproject.views import DepartmentList
from backendproject.models import *
from django.contrib.auth.models import User
from django.utils import timezone
import unittest
# Create your tests here.


# class SimpleTest(TestCase):
#     def test_details(self):
#         data = {
#             'username': 'wang',
#             'password': '123456',
#             'name': 'cat'
#         }
#         response = self.client.post('/api/register', data)
#         self.assertEqual(response.status_code, 200)
#         response_data = response.data
#         print(response_data)
#         self.assertEqual(response_data, data['name'])


class UserModelTest(TestCase):
    def setUp(self):
        User.objects.create(id="2", username="wang", password="123456")
        print("UserModelTest Start!")

    def test_user_model(self):
       # self.assertEqual(DepartmentList(), {[{'department_leader': '1', 'department_name': '人事部'}]})
        result = User.objects.get(id='2')
        self.assertEqual(result.username, "wang")

    def tearDown(self):
        User.objects.get(id=2).delete()
        print("UserModelTest End!")
        print('=============================')


class DepartmentModelTest(TestCase):
    def setUp(self):
        User.objects.create(id='1', username="wang2", password="123456")
        Department.objects.create(id='1', name="人事部", leader_id=1)
        print("DepartmentModelTest Start!")

    def test_department_model(self):
        dep_result = Department.objects.get(id='1')
        self.assertEqual(dep_result.name, "人事部")

    def tearDown(self):
        Department.objects.get(id=1).delete()
        print("DepartmentModelTest End!")
        print('=============================')


class ProjectModelTest(TestCase):
    def setUp(self):
        User.objects.create(id='3', username="wang2", password="123456")
        Department.objects.create(id='2', name="工程部", leader_id='3')
        Project.objects.create(id='1', content="Test", title="长江工程",
                               begin_time=timezone.now(), end_time=timezone.now()+timezone.timedelta(3),
                               department_id='2', leader_id='3')
        print("ProjectModelTest Start!")

    def test_project_model(self):
        result = Project.objects.get(id='1')
        self.assertEqual(result.title, "长江工程")

    def tearDown(self):
        Project.objects.get(id='1').delete()
        print("ProjectModelTest End!")
        print('=============================')


class AdvanceModelTest(TestCase):
    def setUp(self):
        User.objects.create(id='4', username="wang2", password="123456")
        Department.objects.create(id='3', name="工程部", leader_id='4')
        Project.objects.create(id='2', content="Test", title="长江工程",
                               begin_time=timezone.now(), end_time=timezone.now() + timezone.timedelta(3),
                               department_id='3', leader_id='4')
        Advance.objects.create(id='1', category='', title='', number=500, agreement=None,
                               time=timezone.now(), project_id='2')
        print("AdvanceModelTest Start")

    def test_advance_model(self):
        result = Advance.objects.get(id='1')
        self.assertEqual(result.number, 500)

    def tearDown(self):
        Advance.objects.get(id='1').delete()
        print('AdvanceModelTest End')
        print('=============================')


class CompanyModelTest(TestCase):
    def setUp(self):
        Company.objects.create(id=1, name='计蒜客', logo='', time=timezone.now())
        print("CompanyModelTest Start!")

    def test_company_model(self):
        result = Company.objects.get(id=1)
        self.assertEqual(result.name, "计蒜客")

    def tearDown(self):
        print("CompanyModelTest End!")
        print('=============================')


class ConfirmModelTest(TestCase):
    def setUp(self):
        User.objects.create(id='3', username="wang2", password="123456")
        Department.objects.create(id='2', name="工程部", leader_id='3')
        Project.objects.create(id='1', content="Test", title="长江工程",
                               begin_time=timezone.now(), end_time=timezone.now() + timezone.timedelta(3),
                               department_id='2', leader_id='3')
        ConfirmExpend.objects.create(id='1', category='水电费', title='', number=500, agreement='',
                                     time=timezone.now(), project_id='1')
        print("ConfirmModel Start!")

    def test_confirm_model(self):
        result = ConfirmExpend.objects.get(id=1)
        self.assertEqual(result.number, 500)

    def tearDown(self):
        print("ConfirmExpendModel End!")


suite = unittest.TestSuite()
suite.addTest(AdvanceModelTest("test_advance_model"))
suite.addTest(CompanyModelTest("test_company_model"))
suite.addTest(DepartmentModelTest("test_department_model"))
suite.addTest(ProjectModelTest("test_project_model"))
suite.addTest(UserModelTest("test_user_model"))
suite.addTest(ConfirmModelTest("test_confirm_model"))
runner = unittest.TextTestRunner()
runner.run(suite)




