from ..models import Resume
from users.tests.setup import USER_KWARGS
from vacancy.tests.test_models import VacancyModelsTest


class ResumeModelTest(VacancyModelsTest):
    model = Resume
    model_name_plural = 'resumes'
    user_kwargs = USER_KWARGS
