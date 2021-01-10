from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .setup import TestClientsSetUp


class UsersViewsTest(TestClientsSetUp):
    def test_template_used(self):
        mapping = {'signup': 'signup.html', 'login': 'login.html'}
        client = self.unauthorized_client
        self.check_template_used(mapping, client)

    def test_content_is_instance(self):
        mapping = {
            'signup': {'form': UserCreationForm},
            'login': {'form': AuthenticationForm}
        }
        client = self.unauthorized_client
        assertion = self.assertIsInstance
        self.check_context(mapping, client, assertion)
