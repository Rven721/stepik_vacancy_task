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
from django.urls import path

import main.views as mv

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', mv.MainView.as_view(), name="main"),
    path('vacancies/', mv.VacanciesView.as_view(), name='vacancies'),
    path('vacancies/cat/<str:cat_name>', mv.SpecialityView.as_view(), name='vacancies_cat'),
    path('vacancies/<int:vac_id>/', mv.VacancyView.as_view(), name='vacancy'),
    path('companies/<int:comp_id>/', mv.CompanyCardView.as_view(), name='company'),

]
