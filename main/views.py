from django.db.models import Count
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from main.models import Company, Specialty, Vacancy


class MainView(TemplateView):
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['specialties'] = Specialty.objects.annotate(vacancy_count=Count('vacancies'))
        context['companies'] = Company.objects.annotate(company_vacancy_count=Count('companies'))
        return context


class CompanyCardView(TemplateView):
    template_name = 'main/company_card.html'

    def get_context_data(self, comp_id):
        context = super().get_context_data()
        context['vacancies'] = Vacancy.objects.filter(company__id=comp_id)
        context['company'] = get_object_or_404(Company, id=comp_id)
        return context


class VacanciesView(TemplateView):
    template_name = 'main/vacancies.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['vacancies'] = Vacancy.objects.all()
        context['specialties'] = Specialty.objects.annotate(vacancy_count=Count('vacancies'))
        return context


class SpecialityView(TemplateView):
    template_name = 'main/vacancies_speciality.html'

    def get_context_data(self, cat_name):
        """не применяю get_object_or_404 специально, чтобы напомнить сбе, что есть несколько варинтов броскния ошибки"""
        context = super().get_context_data()
        context['title'] = Specialty.objects.filter(code=cat_name)
        context['vacancies'] = Vacancy.objects.filter(specialty__code=cat_name)
        if cat_name not in [cat.code for cat in Specialty.objects.all()]:
            raise Http404
        return context


class VacancyView(TemplateView):
    template_name = 'main/vacancy.html'

    def get_context_data(self, vac_id):
        context = super().get_context_data()
        context['vacancy'] = get_object_or_404(Vacancy, id=vac_id)
        return context
