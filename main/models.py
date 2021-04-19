from datetime import date
from django.contrib.auth.models import User
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from stepik_vacancy_task.settings import MEDIA_COMPANY_IMAGE_DIR, MEDIA_SPECIALITY_IMAGE_DIR


class Company(models.Model):
    name = models.CharField(max_length=120)
    location = models.CharField(max_length=120)
    logo = models.ImageField(default="https://place-hold.it/100x60", upload_to=MEDIA_COMPANY_IMAGE_DIR)
    description = models.TextField()
    employee_count = models.PositiveIntegerField()
    owner = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, related_name='my_company', null=True)

    def __str__(self):
        return f'{self.name}'


class Specialty(models.Model):
    code = models.CharField(max_length=15)
    title = models.CharField(max_length=120)
    picture = models.ImageField(default="https://place-hold.it/100x60", upload_to=MEDIA_SPECIALITY_IMAGE_DIR)

    def __str__(self):
        return f'{self.code} {self.title}'


class Vacancy(models.Model):
    title = models.CharField(max_length=120)
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE, related_name='vacancies')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='companies')
    skills = models.TextField()
    description = models.TextField()
    salary_min = models.PositiveIntegerField()
    salary_max = models.PositiveIntegerField()
    published_at = models.DateField(default=date.today)

    def __str__(self):
        return f'{self.title}'


class Application(models.Model):
    written_username = models.CharField(max_length=120)
    written_phone = PhoneNumberField()
    written_cover_letter = models.TextField()
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, related_name='applications')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')


    def __str__(self):
        return f'{self.user} - {self.vacancy}'


class Resume(models.Model):
    class Status(models.TextChoices):
        NOT_SEARCHING = 'NS', 'Не ищу работу'
        OPEN = 'OP', 'Рассматриваю предложения'
        SEARCHING = 'SE', 'Ищу работу'

    class Grade(models.TextChoices):
        BEGINNER = 'BG', 'Стажер'
        JUNIOR = 'JN', 'Джуниор'
        MIDDL = 'MD', 'Миддл'
        SENIOR = 'SEN', 'Синьор'
        LEAD = 'LE', 'Лид'

    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=False, related_name='my_resume')
    name = models.CharField(max_length=120)
    surname = models.CharField(max_length=120)
    status = models.CharField(max_length=10, choices=Status.choices)
    salary = models.PositiveIntegerField()
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE, related_name='my_vacancy')
    grade = models.CharField(max_length=10, choices=Grade.choices)
    education = models.TextField()
    experience = models.TextField()
    portfolio = models.CharField(max_length=120)

    def __str__(self):
        return f'{self.user} {self.name} {self.surname}'
