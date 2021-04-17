from django.db.models import Count, Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, reverse
from django.views.generic import TemplateView, DetailView, View, ListView

from main.forms import ApplicationForm
from main.models import Company, Specialty, Vacancy, Resume


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
        context['company'] = get_object_or_404(Company, id=comp_id)
        context['vacancies'] = Vacancy.objects.filter(company__id=comp_id)
        return context


class VacanciesView(TemplateView):
    template_name = 'main/vacancies.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['vacancies'] = Vacancy.objects.all()
        return context


class SpecialityView(TemplateView):
    template_name = 'main/vacancies_speciality.html'

    def get_context_data(self, cat_name):
        """не применял get_object_or_404 специально, чтобы напомнить сбе, что есть несколько варинтов бросания ошибки
                if cat_name not in [cat.code for cat in Specialty.objects.all()]:
            raise Http404
        "Проверять наличие нужно с помощью filter или get. Доставать все данные из бд как здесь очень плохой вариант."""
        context = super().get_context_data()
        context['title'] = get_object_or_404(Specialty, code=cat_name)
        context['vacancies'] = Vacancy.objects.filter(specialty__code=cat_name)
        return context


class VacancyView(View):

    def get(self, request, vac_id):
        ctx = {
            'vacancy': get_object_or_404(Vacancy, id=vac_id),
            'form': ApplicationForm,
        }
        return render(request, 'main/vacancy.html', ctx)

    def post(self, request, vac_id):
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.vacancy = Vacancy.objects.filter(id=vac_id).first()
            application.save()
            return HttpResponseRedirect(reverse('send', kwargs={'vac_id': vac_id}))
        ctx = {
            'vacancy': get_object_or_404(Vacancy, id=vac_id),
            'form': form,
        }
        return render(request, 'main/vacancy.html', ctx)


class VacancyView2(DetailView):
    """При использовании такой вьюхи вместо vac_id мы в url должны определить переменную pk(primary key)"""
    model = Vacancy
    template_name = 'main/vacancy.html'


class ApplicationSendView(TemplateView):
    template_name = 'main/application.html'


class ResumeView(DetailView):
    template_name = 'main/resume.html'
    model = Resume
    context_object_name = 'resume'


class VacancySearchView(ListView):
    template_name = 'main/search_results.html'
    context_object_name = 'vacancies'

    def get_queryset(self):
        query = self.request.GET.get('keyword')
        return Vacancy.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(skills__icontains=query) |
            Q(specialty__code__icontains=query) |
            Q(specialty__title__icontains=query),
        )
