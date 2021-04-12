from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, DeleteView

from main.forms import CompanyForm
from main.models import Company


class MyCompanyView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'login'

    def get(self, request):
        company = Company.objects.filter(owner=request.user).first()
        if company is None:
            return render(request, 'main/my_company/lets_start.html')
        ctx = {
            'form': CompanyForm(instance=company),
            'updated_data': False,
            'company': company,
        }
        return render(request, 'main/my_company/my_company.html', ctx)

    def post(self, request):
        company = Company.objects.filter(owner=request.user).first()
        new_data = CompanyForm(request.POST, request.FILES, instance=company)
        if new_data.is_valid():
            company.save()
            ctx = {
                'form': CompanyForm(instance=company),
                'updated_data': True,
            }
            return render(request, 'main/my_company/my_company.html', ctx)
        return render(request, 'main/my_company/my_company.html', {'form': new_data})


class MycompanyCreateView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'login'

    def get(self, request):
        if Company.objects.filter(owner=request.user):
            return HttpResponseRedirect(reverse_lazy('my_company'))
        return render(request, 'main/my_company/my_company.html', {'form': CompanyForm})

    def post(self, request):
        user = request.user
        form = CompanyForm(request.POST, request.FILES)
        if form.is_valid():
            my_company = form.save(commit=False)
            my_company.owner = user
            my_company.save()
            company = Company.objects.filter(owner=user).first()
            ctx = {
                'form': CompanyForm(instance=company),
                'updated_data': True,
                'company': company,
            }
            return render(request, 'main/my_company/my_company.html', ctx)
        return render(request, 'main/my_company/my_company.html', {'form': form})


class LetsStartView(LoginRequiredMixin, TemplateView):
    template_name = 'main/lets_start.html'
    login_url = '/login/'
    redirect_field_name = 'login'


class MyCompanyDeleteView(LoginRequiredMixin, DeleteView):
    login_url = '/login/'
    redirect_field_name = 'login'
    model = Company
    template_name = 'main/my_company/my_company_confirm_delete.html'
    context_object_name = 'company'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.owner != request.user:
            raise Http404
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_success_url(self):
        return reverse_lazy('my_company')
