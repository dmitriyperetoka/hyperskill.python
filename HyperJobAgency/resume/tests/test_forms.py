from ..forms import ResumeForm
from ..models import Resume
from vacancy.tests.setup import TestSetUp


class ResumeFormsTest(TestSetUp):
    def test_form_fields(self):
        form_class = ResumeForm
        fields_list = ['description']
        self.check_form_fields(form_class, fields_list)

    def test_form_data(self):
        client = self.authorized_client
        reverse_name = 'create_resume'
        form_class = ResumeForm
        model = Resume
        self.check_form_data(client, reverse_name, form_class, model)
