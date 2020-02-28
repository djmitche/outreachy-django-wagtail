from django.test import TestCase, override_settings
from .models import FinalApplication
from .scenarios import InitialApplicationsUnderwayScenario


# don't try to use the static files manifest during tests
@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class FinalApplicationTestCase(TestCase):

    @staticmethod
    def make_application_fields():
        text_fields = (
            'experience',
            'foss_experience',
            'relevant_projects',
            'applying_to_gsoc',
            'community_specific_questions',
            'timeline',
        )
        values = {}
        for field in text_fields:
            values[field] = 'this is my {}'.format(field.replace('_', ' '))
        return values

    def test_submit_valid(self):
        scenario = InitialApplicationsUnderwayScenario(round__start_from='contributions_open')

        expected = self.make_application_fields()

        self.client.force_login(scenario.applicant1.applicant.account)
        response = self.client.post(
            scenario.project.get_apply_url(),
            expected,
            # Follow any redirects to other pages after the post, and record a
            # history of where the redirect went to.
            follow=True,
        )

        self.assertRedirects(response, scenario.project.get_contributions_url())

        application = FinalApplication.objects.get(
            applicant=scenario.applicant1,
            project=scenario.project,
        )

        actual = {field: getattr(application, field) for field in expected.keys()}
        self.assertEqual(expected, actual)
