from vacancy.models import AbstractVacancy


class Resume(AbstractVacancy):
    """Store resumes in the database."""

    foreign_key_related_name = 'resumes'
