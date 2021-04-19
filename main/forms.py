from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from django import forms
from tinymce.widgets import TinyMCE

from main.models import Application, Company, Vacancy, Resume


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ('written_username', 'written_phone', 'written_cover_letter')
        labels = {
            'written_username': 'Ваше имя',
            'written_phone': 'Ваш телефон',
            'written_cover_letter': 'Сопроводительное письмо',
        }


class CompanyForm(forms.ModelForm):
    description = forms.CharField(widget=TinyMCE, label='Информация о компании')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper.form_method = 'post'

        self.helper.layout = Layout(
            Row(
                Column('name'),
                Column('logo'),
            ),
            Row(
                Column('employee_count'),
                Column('location'),
            ),
            'description',
            Submit('submit', 'Сохранить'),
        )

    class Meta:
        model = Company
        fields = ('name', 'location', 'logo', 'description', 'employee_count')
        labels = {
            'name': 'Название компании',
            'location': 'География',
            'logo': 'Логотип',
            'description': 'Информация о компании',
            'employee_count': 'Количество человек в компании',
        }


class VacancyForm(forms.ModelForm):
    description = forms.CharField(widget=TinyMCE, label='Описание вакансии')

    def clean(self):
        super().clean()
        salary_min = self.cleaned_data['salary_min']
        salary_max = self.cleaned_data['salary_max']
        if salary_max < salary_min:
            raise forms.ValidationError({'salary_max': 'Сумма не может быть ниже минимальной заработной платы'})

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper.form_method = 'post'

        self.helper.layout = Layout(
            Row(
                Column('title'),
                Column('specialty'),
            ),
            Row(
                Column('salary_min'),
                Column('salary_max'),
            ),
            'skills',
            'description',
            Submit('submit', 'Сохранить'),
        )

    class Meta:
        model = Vacancy
        fields = ('title', 'specialty', 'salary_min', 'salary_max', 'skills', 'description')
        labels = {'title': 'Название вакансии',
                  'specialty': 'Специализация',
                  'skills': 'Требуемые навыки',
                  'description': 'Описание вакансии',
                  'salary_min': 'Зарплата от',
                  'salary_max': 'Зарплата до',
                  }


class ResumeForm(forms.ModelForm):
    education = forms.CharField(widget=TinyMCE, label='Образование')
    experience = forms.CharField(widget=TinyMCE, label='Опыт')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper.form_method = 'post'

        self.helper.layout = Layout(
            Row(
                Column('name'),
                Column('surname'),
            ),
            Row(
                Column('status'),
                Column('salary'),
            ),
            Row(
                Column('specialty'),
                Column('grade'),
            ),
            'education',
            'experience',
            'portfolio',
            Submit('submit', 'Сохранить изменения'),
        )

    class Meta:
        model = Resume
        fields = ('name', 'surname', 'status', 'salary', 'specialty', 'grade', 'education', 'experience', 'portfolio')
        labels = {'name': 'Имя',
                  'surname': 'Фамилия',
                  'status': 'Статус',
                  'salary': 'Заработная плата',
                  'grade': 'Квалификация',
                  'specialty': 'Специализация',
                  'education': 'Образование',
                  'experience': 'Опыт',
                  'portfolio': 'Портфолио',
                  }


class SendMailForm(forms.Form):
    title = forms.CharField(max_length=120, label='Тема')
    email = forms.EmailField(label="От кого")
    to = forms.EmailField(label="Кому")
    message = forms.CharField(widget=TinyMCE, label='Сообщение')
