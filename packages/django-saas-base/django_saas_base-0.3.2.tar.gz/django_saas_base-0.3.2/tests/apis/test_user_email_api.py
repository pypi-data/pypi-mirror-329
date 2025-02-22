from saas_base.models import UserEmail
from tests.client import FixturesTestCase


class TestEmailAPI(FixturesTestCase):
    user_id = FixturesTestCase.EMPTY_USER_ID

    def test_list_emails(self):
        self.force_login()

        url = '/m/user/emails/'
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json(), [])

        for i in range(5):
            UserEmail.objects.create(user=self.user, email=f'demo-{self.user_id}-{i}@example.com')

        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.json()), 5)
