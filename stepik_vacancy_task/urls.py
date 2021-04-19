"""stepik_vacancy_task URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path, include
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static

import main.views.main as mv
import main.views.my_company as company
import main.views.my_vacancy as vacancy
import main.views.my_resume as resume
import accounts.views as av


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', mv.MainView.as_view(), name="main"),
    path('vacancies/', mv.VacanciesView.as_view(), name='vacancies'),
    path('vacancies/cat/<str:cat_name>', mv.SpecialityView.as_view(), name='vacancies_cat'),
    path('vacancies/<int:vac_id>/', mv.VacancyView.as_view(), name='vacancy'),
    path('companies/<int:comp_id>/', mv.CompanyCardView.as_view(), name='company'),
    path('register/', av.MyRegisterView.as_view(), name='register'),
    path('login/', av.MyLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('vacancies/<int:vac_id>/send/', mv.ApplicationSendView.as_view(), name='send'),
    path('mycompany/letsstart/', company.LetsStartView.as_view(), name='letsstart'),
    path('mycompany/create/', company.MycompanyCreateView.as_view(), name='my_company_create'),
    path('mycompany/<int:pk>/delete/', company.MyCompanyDeleteView.as_view(), name='my_company_delete'),
    path('mycompany/', company.MyCompanyView.as_view(), name='my_company'),
    path('mycompany/vacancies/', vacancy.MyVacancies.as_view(), name='my_company_vacancies'),
    path('mycompany/vacancies/create/', vacancy.MyVacancyCreateView.as_view(), name='my_company_vac_create'),
    path('mycompany/vacancies/<int:vac_id>/', vacancy.MyVacancy.as_view(), name='my_company_vacancy'),
    path('mycompany/vacancies/<int:pk>/delete/', vacancy.MyVacancyDeleteView.as_view(), name='my_company_vac_delete'),
    path('applications/<int:vac_id>/', vacancy.ApplicationsListView.as_view(), name='applications_list'),
    path('myresume/', resume.MyResumeView.as_view(), name='my_resume'),
    path('myresume/create/', resume.MyResumeCreate.as_view(), name='my_resume_create'),
    path('myresume/create/success/', resume.MyResumeSuccessView.as_view(), name='my_resume_success'),
    path('myresume/<int:pk>/delete/', resume.MyResumeDeleteView.as_view(), name='my_resume_delete'),
    path('search/', mv.VacancySearchView.as_view(), name='vacancy_search'),
    path('resume/<int:pk>', mv.ResumeView.as_view(), name='resume'),
    path('resume/<int:resume_id>/sendmail/', mv.SendMailView.as_view(), name='send_mail'),
    path('tinymce/', include('tinymce.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
