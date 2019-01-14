# coding=utf-8
from django.test import TestCase
from backendproject.views import DepartmentList
from backendproject.models import *
import unittest
# Create your tests here.


class SimpleTest(TestCase):
    def test_details(self):
        data = {
            'username': 'wang',
            'password': '123456',
            'name': 'cat'
        }
        response = self.client.post('/api/register', data)
        self.assertEqual(response.status_code, 200)
        response_data = response.data
        print(response_data)
        self.assertEqual(response_data, data['name'])


class GetDepartmentTest(TestCase):
    def setUp(self):
        User.objects.create(username="wang", password="123456")
        print("Test Start!")

    def test_get_department(self):
       # self.assertEqual(DepartmentList(), {[{'department_leader': '1', 'department_name': '人事部'}]})
       result = User.objects.get(id='1')
       self.assertEqual(result.username, "wang")
    def tearDown(self):
        User.objects.get(id=1).delete()
        print("Test End!")


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(GetDepartmentTest("test_get_department"))
    runner = unittest.TextTestRunner()
    runner.run(suite)



