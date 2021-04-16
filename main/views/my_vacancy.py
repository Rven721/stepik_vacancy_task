from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import View, DeleteView, TemplateView

from main.forms import VacancyForm
from main.models import Vacancy, Application, Company


class MyVacancies(LoginRequiredMixin, View):
    redirect_field_name = 'login'

    def get(self, request):
        my_vacancies = Vacancy.objects.filter(company__owner=request.user).annotate(app_count=Count('applications'))
        ctx = {
            'my_vacancies': my_vacancies,
        }
        return render(request, 'main/my_vacancy/my_vacancies.html', ctx)


class MyVacancy(LoginRequiredMixin, View):
    redirect_field_name = 'login'

    def get(self, request, vac_id):
        vacancy = get_object_or_404(Vacancy, id=vac_id, company__owner=request.user)
        vacancy_form = VacancyForm(instance=vacancy)
        applications = Application.objects.filter(vacancy__id=vac_id)
        ctx = {
            'vacancy': vacancy,
            'vacancy_form': vacancy_form,
            'applications': applications,
        }
        return render(request, 'main/my_vacancy/my_vacancy.html', ctx)

    def post(self, request, vac_id):
        vacancy = get_object_or_404(Vacancy, id=vac_id, company__owner=request.user)
        applications = Application.objects.filter(vacancy__id=vac_id)
        vacancy_data_form = VacancyForm(request.POST, instance=vacancy)
        if vacancy_data_form.is_valid():
            vacancy.save()
            messages.success(request, 'Данные обновлены!')
            return redirect('my_company_vacancy', vac_id)
        ctx = {
            'vacancy_form': vacancy_data_form,
            'applications': applications,
        }
        messages.error(request, "Данные не обновлены!")
        return render(request, 'main/my_vacancy/my_vacancy.html', ctx)


class MyVacancyCreateView(LoginRequiredMixin, View):
    redirect_field_name = 'login'

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
        messages.error(request, 'В форме допущены ошибки!')
        return render(request, 'main/my_vacancy/my_vacancy.html', ctx)


class MyVacancyDeleteView(LoginRequiredMixin, DeleteView):
    redirect_field_name = 'login'
    model = Vacancy
    template_name = 'main/my_vacancy/my_vacancy_confirm_delete.html'
    context_object_name = 'vacancy'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.company.owner != request.user:
            raise Http404
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_success_url(self):
        return reverse_lazy('my_company_vacancies')


class ApplicationsListView(LoginRequiredMixin, TemplateView):
    redirect_field_name = 'login'
    template_name = 'main/my_vacancy/application_list.html'

    def get_context_data(self, vac_id):
        context = super().get_context_data()
        context['applications'] = Application.objects.filter(vacancy__id=vac_id)
        return context
