from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

User = get_user_model()

USER_KWARGS = {
    'username': 'justanotheruser',
    'password': 'Justanotherpassword123',
}

STAFF_USER_KWARGS = {
    'username': 'justanotherstaffuser',
    'password': 'Justanotherstaffpassword123',
    'is_staff': True,
}


class TestSetUp(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(**USER_KWARGS)
        cls.staff_user = User.objects.create_user(**STAFF_USER_KWARGS)

        cls.unauthorized_client = Client()

        cls.authorized_client = Client(default_user=cls.user)
        cls.authorized_client.force_login(cls.user)

        cls.authorized_staff_client = Client(default_user=cls.staff_user)
        cls.authorized_staff_client.force_login(cls.staff_user)

        cls.authorized_clients = [
            cls.authorized_client,
            cls.authorized_staff_client,
        ]

        cls.clients = cls.authorized_clients + [cls.unauthorized_client]

    def check_status_code(self, urls, client, status_code):
        for url in urls:
            response = client.get(url)

            with self.subTest():
                self.assertEqual(response.status_code, status_code)

    def check_exists(self, urls, client):
        return self.check_status_code(urls, client, status_code=200)

    def check_not_allowed(self, urls, client):
        return self.check_status_code(urls, client, status_code=405)

    def check_redirects(self, mapping, client):
        for url, redirect_url in mapping.items():
            with self.subTest():
                response = client.get(url)
                self.assertRedirects(response, redirect_url)

    def check_redirect_chain(self, mapping, client):
        for url, redirect_chain in mapping.items():
            with self.subTest():
                response = client.get(url, follow=True)
                self.assertEqual(response.redirect_chain, redirect_chain)

    def check_template_used(self, mapping, client):
        for reverse_name, template in mapping.items():
            response = client.get(reverse(reverse_name))

            with self.subTest():
                self.assertTemplateUsed(response, template)

    def check_context(self, mapping, client, assertion):
        for reverse_name, context in mapping.items():
            response = client.get(reverse(reverse_name))

            for key, value in context.items():
                with self.subTest():
                    assertion(response.context.get(key), value)

    def check_context_object_list(self, client, reverse_name, model):
        model.objects.create(
            author=client.defaults['default_user'],
            description='Just another description.'
        )
        response = client.get(reverse(reverse_name))
        object_list = response.context.get('object_list')
        self.assertEqual(list(object_list), list(model.objects.all()))

    def check_created(self, client, response, count_difference, model, kwargs):
        redirect_url = '/home/'

        with self.subTest():
            self.assertRedirects(response, redirect_url)

        with self.subTest():
            self.assertEqual(count_difference, 1)

        new_obj = model.objects.get(**kwargs)
        request_user = client.defaults['default_user']

        with self.subTest():
            self.assertEqual(new_obj.author, request_user)

    def check_object_create(self, client, reverse_name, model):
        kwargs = {'description': 'Just another description.'}

        with self.subTest():
            self.assertFalse(model.objects.filter(**kwargs).exists())

        initial_count = model.objects.count()

        another_client = [q for q in self.authorized_clients if q != client][0]

        response = another_client.post(reverse(reverse_name), kwargs)
        count_difference = model.objects.count() - initial_count

        with self.subTest():
            self.assertEqual(response.status_code, 403)

        with self.subTest():
            self.assertEqual(count_difference, 0)

        response = self.unauthorized_client.post(reverse(reverse_name), kwargs)
        count_difference = model.objects.count() - initial_count

        redirect_url = f'/login?next=/{model.__name__.lower()}/new'

        with self.subTest():
            self.assertRedirects(response, redirect_url)

        with self.subTest():
            self.assertEqual(count_difference, 0)

        response = client.post(reverse(reverse_name), kwargs)
        count_difference = model.objects.count() - initial_count
        self.check_created(client, response, count_difference, model, kwargs)

    def check_form_fields(self, form_class, fields_list):
        form = form_class()
        self.assertEqual(list(form.fields), fields_list)

    def check_form_data(self, client, reverse_name, form_class, model):
        kwargs = {'description': 'Just another description.'}
        form = form_class(kwargs)
        initial_count = model.objects.count()
        response = client.post(reverse(reverse_name), data=form.data)
        count_difference = model.objects.count() - initial_count
        self.check_created(client, response, count_difference, model, kwargs)
