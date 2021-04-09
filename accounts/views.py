from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView

from accounts.forms import MyRegisterForm


# Create your views here.


class MyLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True


class MyRegisterView(CreateView):
    form_class = MyRegisterForm
    model = User
    template_name = 'accounts/register.html/'
    success_url = '/login/'
