from django.test import TestCase

from ..models import User, Vacancy
from users.tests.setup import STAFF_USER_KWARGS


class VacancyModelsTest(TestCase):
    model = Vacancy
    model_name_plural = 'vacancies'
    user_kwargs = STAFF_USER_KWARGS

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(**cls.user_kwargs)
        cls.model_instance = cls.model.objects.create(
            author=cls.user,
            description=" ".join(['just another description.'] * 39)
        )

    def test_foreign_key_related_name(self):
        related_name = self.model.foreign_key_related_name
        self.assertEqual(related_name, self.model_name_plural)

    def test_author_cascade(self):
        self.assertEqual(self.model.objects.count(), 1)

        self.user.delete()

        self.assertEqual(self.model.objects.count(), 0)

    def test_description_attributes(self):
        attributes = {
            'verbose_name': 'Description',
            'max_length': 1024,
            'help_text': 'Fill in the description here.',
        }

        for attribute, expected_value in attributes.items():
            with self.subTest():
                attribute_value = (
                    self.model_instance._meta.get_field(
                        'description'
                    ).__getattribute__(attribute)
                )
                self.assertEqual(attribute_value, expected_value)

    def test_str(self):
        self.assertEqual(
            str(self.model_instance), self.model_instance.description[:25]
        )
