"""
Goal: test the client visiting the /oauth/token page
    in order to get an access token.

Authors:
    Andrei Sura <sura.andrei@gmail.com>

"""
from base_test_with_data import BaseTestCaseWithData
from olass.main import app


token_request_url = 'https://localhost/oauth/token'
private_url = 'https://localhost/api/me'


class TestOauth(BaseTestCaseWithData):

    def test_me(self):
        """
        Verify that without an access token we can't access
        restricted routes.
        """

        with self.app.test_request_context():
            with app.test_client() as client:
                print("Request restricted resource using GET: {}"
                      .format(private_url))
                response = client.get(private_url)
                self.assert401(response)
                self.assertEqual('401 UNAUTHORIZED', response.status)

    def test_request_access_token(self):
        """
        Verify that we can request an access token and use it
        to access a restricted resource.
        """
        token_request_data_ok = {
            'client_id': 'client_1',
            'client_secret': 'secret_1',
            'grant_type': 'client_credentials'
        }
        token_request_data_fail = {
            'client_id': 'client_1',
            'client_secret': '',
        }

        wsgi_env = {
            'REMOTE_ADDR': '1.2.3.4',
            'HTTP_USER_AGENT': 'UnitTester',
        }

        with self.app.test_request_context(environ_base=wsgi_env):
            with app.test_client() as client:

                # verify that not specifying a `client_secret`
                # results in a `401 Unauthorized` response
                with self.assertRaises(Exception):
                    response_fail = client.post(token_request_url,
                                                data=token_request_data_fail)
                    self.assert401(response_fail)

                # Trigger execution of before_request()
                # app.preprocess_request()
                print("\nRequest access from: {}".format(token_request_url))
                response = client.post(token_request_url,
                                       data=token_request_data_ok)
                access_token = response.json.get('access_token')
                print("Retrieved access token: {}".format(access_token))

                # Now use the retrieved access token
                query_data = {'access_token': access_token}
                response = client.get(private_url, data=query_data)

                print("Response code: {}, status: {}"
                      .format(response.status_code, response.status))

                self.assert200(response, "Response code is not 200")

                if 200 == response.status_code:
                    data = response.json.get('data')
                    print("Response: {}".format(data))
                    self.assertEqual('test@test.com',
                                     data.get('user')['email'])
                else:
                    self.fail("This should no happen")


if __name__ == '__main__':
    import unittest
    unittest.main()

"""
Response attributes:
    'json',
    'last_modified',
    'location',
    'make_conditional',
    'make_sequence',
    'mimetype',
    'mimetype_params',
    'response',
    'retry_after',
    'set_cookie',
    'set_data',
    'set_etag',
    'status',
    'status_code',
    'stream',
    'vary',
    'www_authenticate'
"""
