from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import View, DeleteView, TemplateView

from main.forms import ResumeForm
from main.models import Resume


class MyResumeView(View):

    def get(self, request):
        resume = Resume.objects.filter(user=request.user).first()
        if resume is None:
            return render(request, 'main/my_resume/my_resume_lets_start.html')
        ctx = {
            'resume': resume,
            'resume_data': ResumeForm(instance=resume),
            'update_flag': False,
        }
        return render(request, 'main/my_resume/my_resume.html', ctx)

    def post(self, request):
        resume = Resume.objects.filter(user=request.user).first()
        resume_data = ResumeForm(request.POST)
        if resume_data.is_valid():
            updated_resume_data = resume_data.cleaned_data
            resume.name = updated_resume_data['name']
            resume.surname = updated_resume_data['surname']
            resume.status = updated_resume_data['status']
            resume.salary = updated_resume_data['salary']
            resume.specialty = updated_resume_data['specialty']
            resume.grade = updated_resume_data['grade']
            resume.education = updated_resume_data['education']
            resume.experience = updated_resume_data['experience']
            resume.portfolio = updated_resume_data['portfolio']
            resume.save()
            ctx = {
                'resume': resume,
                'resume_data': ResumeForm(instance=resume),
                'update_flag': True,
            }
            return render(request, 'main/my_resume/my_resume.html', ctx)
        ctx = {
            'resume': resume,
            'resume_data': resume_data,
            'update_flag': False,
        }
        return render(request, 'main/my_resume/my_resume.html', ctx)


class MyResumeCreate(View):

    def get(self, request):
        if Resume.objects.filter(user=request.user):
            return HttpResponseRedirect(reverse_lazy('my_resume'))
        ctx = {'resume_data': ResumeForm,
               'resume': Resume.objects.filter(user=request.user).first()}
        return render(request, 'main/my_resume/my_resume.html', ctx)

    def post(self, request):
        resume_data = ResumeForm(request.POST)
        if resume_data.is_valid():
            resume = resume_data.save(commit=False)
            resume.user = request.user
            resume.save()
            return HttpResponseRedirect(reverse('my_resume_success'))
        ctx = {
            'resume_data': resume_data,
            'update_flag': False,
        }
        return render(request, 'main/my_resume/my_resume.html', ctx)


class MyResumeSuccessView(TemplateView):
    template_name = 'main/my_resume/my_resume_success.html'


class MyResumeDeleteView(DeleteView):
    template_name = 'main/my_resume/my_resume_confirm_delete.html'
    model = Resume
    context_object_name = 'resume'

    def get_success_url(self):
        return reverse_lazy('my_resume')
