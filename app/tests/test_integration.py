"""
Goal: emulate a client submitting data

Authors:
    Andrei Sura <sura.andrei@gmail.com>

"""
from mock import patch
from base_test_with_data import BaseTestCaseWithData
from olass.main import app
from olass import utils

login_url = 'https://localhost/'

# The route for requesting access tokens
token_request_url = 'https://localhost/oauth/token'

# The route for saving chunks
save_patient_chunks_url = 'https://localhost/api/save'

token_request_data_ok = {
    'client_id': 'client_1',
    'client_secret': 'secret_1',
    'grant_type': 'client_credentials'
}

chunks = """
{
"data": {
   "1": {
       "1": "b2cdaea3d7c9891b2ed94d1973fe5085183e4bb4bd87b672e066a456ee67bd38"
       },

   "2": {
       "1": "345b192ae4093dcbc5c914bdcb5e8c41e58162475a295c88b1ce594bd3dd78f7",
       "2": "1dcce10470c0ea73a8a6287f69f4f862c5e13faea7c11104fae07dbc8d5ce56e"
       },
   "3": {
       "1": "995b192ae4093dcbc5c914bdcb5e8c41e58162475a295c88b1ce594bd3dd78f7"
       }
   }
}
"""

# Example of output json:
out = """
{
    "data": {
        "1": {
            "uuid": "ebd9ae1a1ba011e694c84d46767d11db"
        },
        "2": {
            "uuid": "ebd9b9d21ba011e694c84d46767d11db"
        }
    },
    "status": "success"
}
"""


class TestIntegration(BaseTestCaseWithData):

    @patch.multiple(utils,
                    get_uuid_hex=BaseTestCaseWithData.dummy_get_uuid_hex)
    def test_success(self):

        with self.app.test_request_context():
            with app.test_client() as client:
                # print("\n Request access from:{}" .format(token_request_url))
                response = client.post(token_request_url,
                                       data=token_request_data_ok)
                access_token = response.json.get('access_token')
                # print("Retrieved access token: {}".format(access_token))

                # Now use the retrieved access token
                auth_headers = [
                    ('Authorization', "Basic: {}".format(access_token)),
                    ('Content-Type', 'application/json')]

                # Test_1 bad json
                bad_response = client.post(save_patient_chunks_url,
                                           data='{"a": "b",}',
                                           headers=auth_headers)
                # Verify that we get a "400 BAD REQUEST"
                # response for invalid json
                self.assert400(bad_response, "Response code is not 400")

                # Test_2 KeyError 'data'
                with self.assertRaises(Exception):
                    bad_response = client.post(save_patient_chunks_url,
                                               data='{"partner_code": "UF"}',
                                               headers=auth_headers)

                # Test_3 valid request
                response = client.post(save_patient_chunks_url,
                                       data=chunks,
                                       headers=auth_headers)

                self.assert200(response, "Response code is not 200")
                data = response.json.get('data')
                # print("==> Integration test response: {}".format(data))
                status = response.json.get('status')

                if 'success' == status:
                    group_1 = data.get('1')
                    group_2 = data.get('2')
                    group_3 = data.get('3')

                    # compare the UUIDs generated using
                    # base_test_with_data#dummy_get_uuid_hex()
                    self.assertEqual(
                        group_1.get('uuid'),
                        '709949141ba811e69454f45c898e9b67')

                    self.assertEqual(
                        group_2.get('uuid'),
                        '809949141ba811e69454f45c898e9b67')

                    self.assertEqual(
                        group_3.get('uuid'),
                        '109949141ba811e69454f45c898e9b67')
                else:
                    self.fail("Error response: {}".format(data))

    def test_login_form_display(self):
        """
        Check the login form message presence
        """
        with self.app.test_request_context():
            with app.test_client() as client:
                response = client.get(login_url)
                self.assertTrue(b'Please login' in response.data)

    def test_access_protected_resource(self):
        """
        Verify that when not logged in the user is
        unable to access the protected content.
        """
        with self.app.test_request_context():
            with app.test_client() as client:
                response = client.get("https://localhost/api/hello")
                self.assertTrue(b'Please <a href="/">login</a> first.'
                                in response.data)

    def test_login_failure(self):
        """
        Try to login with an invalid password
        """
        login_data = {'email': 'asura-root@ufl.edu',
                      'password': 'invalid-password'}

        with self.app.test_request_context():
            with app.test_client() as client:
                response = client.post(login_url, data=login_data,
                                       follow_redirects=True)
                self.assert200(response, "Response code is not 200")
                self.assertTrue(b'Please login' in response.data)
                self.assertTrue(b'Hello asura-root@ufl.edu'
                                not in response.data)

    def test_login_success(self):
        """
        Emulate user login
        """
        login_data = {'email': 'asura-root@ufl.edu',
                      'password': 'password'}

        with self.app.test_request_context():
            with app.test_client() as client:
                app.preprocess_request()
                response = client.post(login_url, data=login_data,
                                       follow_redirects=True)
                self.assert200(response, "Response code is not 200")
                self.assertTrue(b'Hello asura-root@ufl.edu' in response.data)


if __name__ == '__main__':
    import unittest
    unittest.main()
