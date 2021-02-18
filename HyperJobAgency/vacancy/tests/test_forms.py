from ..forms import VacancyForm
from ..models import Vacancy
from .setup import TestSetUp


class VacancyFormsTest(TestSetUp):
    def test_form_fields(self):
        form_class = VacancyForm
        fields_list = ['description']
        self.check_form_fields(form_class, fields_list)

    def test_form_data(self):
        client = self.authorized_staff_client
        reverse_name = 'create_vacancy'
        form_class = VacancyForm
        model = Vacancy
        self.check_form_data(client, reverse_name, form_class, model)
