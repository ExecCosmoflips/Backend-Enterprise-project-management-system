"""FinancialManagement URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from backendproject import views
from django.urls import path
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import TemplateView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',TemplateView.as_view(template_name='index.html')),
    url(r'api/get_project_list', views.ProjectList.as_view()),
    url(r'api/login', views.Login.as_view()),
    path('api/get_info', views.Login.as_view()),
    path('api/get_project_info', views.ProjectInfo.as_view()),
    path('api/get_project_personnel_info', views.PersonnelInfo.as_view()),
    path('api/get_department_staff', views.DepartmentStaff.as_view()),
    path('api/get_department_list', views.DepartmentList.as_view()),
    path('api/addreceivable', views.AddReceivable.as_view()),
    path('api/add_department_admin', views.getAddDepartmentAdmin.as_view()),
    path('api/get_project_bar_data', views.GetProjectBarData.as_view()),
    path('api/get_project_pie_data', views.GetProjectPieData.as_view()),
    path('api/set_logo', views.SetLogo.as_view()),
    path('api/save_error_logger', views.ErrorLogger.as_view()),
    path('api/send_email', views.SendEmail.as_view()),
    path('api/register', views.Register.as_view()),
    path('api/get_all_staff', views.AllStaffs.as_view()),
    path('api/change_staff', views.ChangeStaff.as_view()),
    path('api/user_request', views.UserRequest.as_view())

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
