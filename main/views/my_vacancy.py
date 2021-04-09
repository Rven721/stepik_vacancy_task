from django.db.models import Count
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import View, DeleteView, TemplateView
from main.models import Vacancy, Application, Company
from main.forms import VacancyForm


class MyVacancies(View):

    def get(self, request):
        my_vacancies = Vacancy.objects.filter(company__owner=request.user).annotate(app_count=Count('applications'))
        ctx = {
            'my_vacancies': my_vacancies,
        }
        return render(request, 'main/my_vacancy/my_vacancies.html', ctx)


class MyVacancy(View):

    def get(self, request, vac_id):
        vacancy = Vacancy.objects.filter(id=vac_id).first()
        if request.user != vacancy.company.owner:
            raise Http404
        vacancy_form = VacancyForm(instance=vacancy)
        applications = Application.objects.filter(vacancy__id=vac_id)
        ctx = {
            'vacancy': vacancy,
            'vacancy_form': vacancy_form,
            'applications': applications,
            'updated_vacancy_data': False,
        }
        return render(request, 'main/my_vacancy/my_vacancy.html', ctx)

    def post(self, request, vac_id):
        vacancy = Vacancy.objects.filter(id=vac_id).first()
        applications = Application.objects.filter(vacancy__id=vac_id)
        vacancy_data_form = VacancyForm(request.POST)
        if vacancy_data_form.is_valid():
            new_vac_data = vacancy_data_form.cleaned_data
            vacancy.title = new_vac_data['title']
            vacancy.specialty = new_vac_data['specialty']
            vacancy.skills = new_vac_data['skills']
            vacancy.description = new_vac_data['description']
            vacancy.salary_min = new_vac_data['salary_min']
            vacancy.salary_max = new_vac_data['salary_max']
            vacancy.save()
            ctx = {
                'vacancy': vacancy,
                'vacancy_form': VacancyForm(instance=vacancy),
                'applications': applications,
                'updated_vacancy_data': True,
            }
            return render(request, 'main/my_vacancy/my_vacancy.html', ctx)
        ctx = {
            'vacancy_form': vacancy_data_form,
            'applications': applications,
            'updated_vacancy_data': False,
        }
        return render(request, 'main/my_vacancy/my_vacancy.html', ctx)


class MyVacancyCreateView(View):

    def get(self, request):
        ctx = {'vacancy_form': VacancyForm}
        return render(request, 'main/my_vacancy/my_vacancy.html', ctx)

    def post(self, request):
        vacancy_data = VacancyForm(request.POST)
        ctx = {'vacancy_form': vacancy_data}
        if vacancy_data.is_valid():
            new_vacancy = vacancy_data.save(commit=False)
            new_vacancy.company = Company.objects.filter(owner=request.user).first()
            new_vacancy.save()
            return HttpResponseRedirect(reverse('my_company_vacancies'))
        return render(request, 'main/my_vacancy/my_vacancy.html', ctx)


class MyVacancyDeleteView(DeleteView):
    model = Vacancy
    template_name = 'main/my_vacancy/my_vacancy_confirm_delete.html'
    context_object_name = 'vacancy'

    def get_success_url(self):
        return reverse_lazy('my_company_vacancies')


class ApplicationsListView(TemplateView):
    template_name = 'main/my_vacancy/application_list.html'

    def get_context_data(self, vac_id):
        context = super().get_context_data()
        context['applications'] = Application.objects.filter(vacancy__id=vac_id)
        return context
