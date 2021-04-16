from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import View, DeleteView, TemplateView

from main.forms import ResumeForm
from main.models import Resume


class MyResumeView(LoginRequiredMixin, View):
    redirect_field_name = 'login'

    def get(self, request):
        if Resume.objects.filter(user=request.user).first() is None:
            return render(request, 'main/my_resume/my_resume_lets_start.html')
        resume = get_object_or_404(Resume, user=request.user)
        ctx = {
            'resume': resume,
            'resume_data': ResumeForm(instance=resume),
            'update_flag': False,
        }
        return render(request, 'main/my_resume/my_resume.html', ctx)

    def post(self, request):
        resume = Resume.objects.filter(user=request.user).first()
        resume_data = ResumeForm(request.POST, instance=resume)
        if resume_data.is_valid():
            resume.save()
            messages.success(request, 'Данные обновлены!')
            return redirect('my_resume')
        ctx = {
            'resume': resume,
            'resume_data': resume_data,
        }
        messages.error(request, 'Данные не обновлены!')
        return render(request, 'main/my_resume/my_resume.html', ctx)


class MyResumeCreate(LoginRequiredMixin, View):
    redirect_field_name = 'login'

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
        ctx = {'resume_data': resume_data,}
        return render(request, 'main/my_resume/my_resume.html', ctx)


class MyResumeSuccessView(TemplateView):
    template_name = 'main/my_resume/my_resume_success.html'


class MyResumeDeleteView(LoginRequiredMixin, DeleteView):
    redirect_field_name = 'login'
    template_name = 'main/my_resume/my_resume_confirm_delete.html'
    model = Resume
    context_object_name = 'resume'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.user != request.user:
            raise Http404
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_success_url(self):
        return reverse_lazy('my_resume')
