# coding=utf-8
from django.test import TestCase
from backendproject.views import DepartmentList
from backendproject.models import *
from django.contrib.auth.models import User
from django.utils import timezone
import unittest
# Create your tests here.


class RegisterAPITest(TestCase):
    def setUp(self):
        User.objects.create(id='3', username="wang2", password="123456")
        Department.objects.create(id='2', name="工程部", leader_id='3')
        UserProfile.objects.create(id='1', access='0', license='0', name='test',
                                   gender='0', email='test@qq.com', phone='110',
                                   department_id='2', user_id='3')
        print("RegisterAPITest Start!")

    def test_register_api(self):
        data = {
            'user': '3',
            'username': 'wang',
            'password': '123456',
            'name': 'cat'
        }
        response = self.client.post('/api/register', data)
        self.assertEqual(response.status_code, 200)
        response_data = response.data
        print(response_data)
        #self.assertEqual(response_data, data['name'])

    def tearDown(self):
        #User.objects.get(id=2).delete()
        print("RegisterAPITest End!")
        print('=============================')



class IncomeTitleListApiTest(TestCase):
    def setUp(self):
        User.objects.create(id='3', username="wang2", password="123456")
        Department.objects.create(id='2', name="工程部", leader_id='3')
        Project.objects.create(id='1', content="Test", title="长江工程",
                               begin_time=timezone.now(), end_time=timezone.now() + timezone.timedelta(3),
                               department_id='2', leader_id='3')
        Income.objects.create(id='1', category="test", project_id='1', title='test',
                              agreement='', time=timezone.now(), confirm_num='0', tax_rate='0')
        print("IncomeTitleListApiTest Start!")

    def test_income_list(self):
        data = {
            'project_id': '1'
        }
        response = self.client.get('/api/get_income_title_list', data)
        self.assertEqual(response.status_code, 200)
        # response_data = response.data
        # print(response_data)
        #self.assertEqual(response_data, data['name'])

    def tearDown(self):
        print("IncomeTitleListApiTest End!")


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
        print('=============================')


class FinancialModelTest(TestCase):

    def setUp(self):
        User.objects.create(id='3', username="wang2", password="123456")
        Department.objects.create(id='2', name="工程部", leader_id='3')
        Project.objects.create(id='1', content="Test", title="长江工程",
                               begin_time=timezone.now(), end_time=timezone.now() + timezone.timedelta(3),
                               department_id='2', leader_id='3')
        FinancialModel.objects.create(id='1', name="测试", number=500, status='0', project_id='1')
        print("FinancialModelTest Start!")

    def test_financial_model(self):
        result = FinancialModel.objects.get(id='1')
        self.assertEqual(result.name, "测试")

    def tearDown(self):
        print("FinancialModelTest End!")
        print('=============================')


class ExpendModelTest(TestCase):

    def setUp(self):
        User.objects.create(id='3', username="wang2", password="123456")
        Department.objects.create(id='2', name="工程部", leader_id='3')
        Project.objects.create(id='1', content="Test", title="长江工程",
                               begin_time=timezone.now(), end_time=timezone.now() + timezone.timedelta(3),
                               department_id='2', leader_id='3')
        FinancialModel.objects.create(id='1', name="测试", number=500, status='0', project_id='1')
        Expend.objects.create(id='1', title="test", number=500, agreement='', time=timezone.now(),
                              category_id='1', project_id='1')

        print("ExpendModelTest Start!")

    def test_expend_model(self):
        result = Expend.objects.get(id='1')
        self.assertEqual(result.title, "test")

    def tearDown(self):
        print("ExpendModelTest End!")
        print('=============================')


class RequestModelTest(TestCase):

    def setUp(self):
        User.objects.create(id='3', username="wang2", password="123456")
        Department.objects.create(id='2', name="工程部", leader_id='3')
        Project.objects.create(id='1', content="Test", title="长江工程",
                               begin_time=timezone.now(), end_time=timezone.now() + timezone.timedelta(3),
                               department_id='2', leader_id='3')
        StaffRequest.objects.create(id='1', whether='0', content='test', project_id='1',
                                    staff_id='3')

        print("RequestModelTest Start!")

    def test_request_model(self):
        result = StaffRequest.objects.get(id="1")
        self.assertEqual(result.content, 'test')

    def tearDown(self):
        print("RequestModelTest End!")
        print('=============================')


class ReceivableModelTest(TestCase):
    def setUp(self):
        User.objects.create(id='3', username="wang2", password="123456")
        Department.objects.create(id='2', name="工程部", leader_id='3')
        Project.objects.create(id='1', content="Test", title="长江工程",
                               begin_time=timezone.now(), end_time=timezone.now() + timezone.timedelta(3),
                               department_id='2', leader_id='3')
        FinancialModel.objects.create(id='1', name="测试", number=500, status='0', project_id='1')
        Receivable.objects.create(id='1', project_id='1', category_id='1', title='test',
                                  number=500, agreement='', time=timezone.now(), advance_state='0',
                                  income_state='0')
        print("ReceivableModelTest Start!")

    def test_receivable_model(self):
        result = Receivable.objects.get(id='1')
        self.assertEqual(result.title, 'test')

    def tearDown(self):
        print("ReceivableModelTest End!")
        print('=============================')


class ProfileModelTest(TestCase):
    def setUp(self):
        User.objects.create(id='3', username="wang2", password="123456")
        Department.objects.create(id='2', name="工程部", leader_id='3')
        UserProfile.objects.create(id='1', access='0', license= '0', name='test',
                                   gender='0', email='test@qq.com', phone='110',
                                   department_id='2', user_id='3')
        print("ProfileModelTest Start!")

    def test_profile_model(self):
        result = UserProfile.objects.get(id='1')
        self.assertEqual(result.name, 'test')

    def tearDown(self):
        print("ProfileModelTest End!")
        print('=============================')


class IncomeModelTest(TestCase):
    def setUp(self):
        User.objects.create(id='3', username="wang2", password="123456")
        Department.objects.create(id='2', name="工程部", leader_id='3')
        Project.objects.create(id='1', content="Test", title="长江工程",
                               begin_time=timezone.now(), end_time=timezone.now() + timezone.timedelta(3),
                               department_id='2', leader_id='3')
        Income.objects.create(id='1', category="test", project_id='1', title='test',
                              agreement='', time=timezone.now(), confirm_num='0', tax_rate='0')
        print("IncomeModelTest Start!")

    def test_income_model(self):
        result = Income.objects.get(id='1')
        self.assertEqual(result.category, "test")

    def tearDown(self):
        print("IncomeModelTest End!")
        print('=============================')


suite = unittest.TestSuite()
suite.addTest(AdvanceModelTest("test_advance_model"))
suite.addTest(CompanyModelTest("test_company_model"))
suite.addTest(DepartmentModelTest("test_department_model"))
suite.addTest(ProjectModelTest("test_project_model"))
suite.addTest(UserModelTest("test_user_model"))
suite.addTest(ConfirmModelTest("test_confirm_model"))
suite.addTest(FinancialModelTest("test_financial_model"))
suite.addTest(ExpendModelTest("test_expend_model"))
suite.addTest(RequestModelTest("test_request_model"))
suite.addTest(ReceivableModelTest("test_receivable_model"))
suite.addTest(ProfileModelTest("test_profile_model"))
suite.addTest(IncomeModelTest("test_income_model"))
suite.addTest(RegisterAPITest("test_register_api"))
suite.addTest(IncomeTitleListApiTest("test_income_list"))
runner = unittest.TextTestRunner()
runner.run(suite)




