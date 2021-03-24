import os

import django

os.environ["DJANGO_SETTINGS_MODULE"] = 'stepik_vacancy_task.settings'
django.setup()

from main.data import jobs, companies, specialties
from main.models import Company, Specialty, Vacancy

if __name__ == '__main__':
    Company.objects.all().delete()
    Specialty.objects.all().delete()
    Vacancy.objects.all().delete()
    company_map = {}
    for company in companies:
        company_map[company['id']] = Company.objects.create(
            name=company['title'],
            location=company['location'],
            logo=company['logo'],
            description=company['description'],
            employee_count=company['employee_count'],
        )
    for specialty in specialties:
        Specialty.objects.create(
            code=specialty['code'],
            title=specialty['title'],
        )
    for vacancy in jobs:
        Vacancy.objects.create(
            title=vacancy['title'],
            specialty=Specialty.objects.get(code=vacancy['specialty']),
            company=company_map[vacancy['company']],
            skills=vacancy['skills'],
            description=vacancy['description'],
            salary_min=vacancy['salary_from'],
            salary_max=vacancy['salary_to'],
            published_at=vacancy['posted'],
        )
