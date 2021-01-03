from vacancy.models import AbstractVacancy


class Resume(AbstractVacancy):
    author_field_related_name = 'resumes'
