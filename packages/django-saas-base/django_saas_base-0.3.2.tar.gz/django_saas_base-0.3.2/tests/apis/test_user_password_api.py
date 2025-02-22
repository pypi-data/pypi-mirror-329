from saas_base.test import SaasTestCase


class TestUserPasswordAPI(SaasTestCase):
    user_id = SaasTestCase.OWNER_USER_ID

    def send_request(self, data):
        self.force_login()
        url = '/m/user/password/'
        return self.client.post(url, data=data, format='json')

    def test_update_password(self):
        data = {"password": "abc12.3D", "confirm_password": "abc12.3D"}
        resp = self.send_request(data)
        self.assertEqual(resp.status_code, 204)

    def test_not_match_password(self):
        data = {"password": "abc12.3D", "confirm_password": "abc12.3C"}
        resp = self.send_request(data)
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.json()['password'], ["Password does not match."])

    def test_too_simple_password(self):
        data = {"password": "foo", "confirm_password": "foo"}
        resp = self.send_request(data)
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(
            resp.json()['password'],
            ["This password is too short. It must contain at least 8 characters."]
        )
