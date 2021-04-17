from django.contrib import admin

# Register your models here.
from main.models import Vacancy, Specialty, Company, Application, Resume

admin.site.register(Vacancy)
admin.site.register(Company)
admin.site.register(Specialty)
admin.site.register(Application)
admin.site.register(Resume)
