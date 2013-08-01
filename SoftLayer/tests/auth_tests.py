"""
    SoftLayer.tests.auth_tests
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2013, SoftLayer Technologies, Inc. All rights reserved.
    :license: BSD, see LICENSE for more details.
"""
try:
    import unittest2 as unittest
except ImportError:
    import unittest  # NOQA

from SoftLayer.auth import (
    AuthenticationBase, BasicAuthentication, TokenAuthentication)


class TestAuthenticationBase(unittest.TestCase):
    def test_get_headers(self):
        auth = AuthenticationBase()
        self.assertRaises(NotImplementedError, auth.get_headers)


class TestBasicAuthentication(unittest.TestCase):
    def setUp(self):
        self.auth = BasicAuthentication('USERNAME', 'APIKEY')

    def test_attribs(self):
        self.assertEquals(self.auth.username, 'USERNAME')
        self.assertEquals(self.auth.api_key, 'APIKEY')

    def test_get_headers(self):
        self.assertEquals(self.auth.get_headers(), {
            'authenticate': {
                'username': 'USERNAME',
                'apiKey': 'APIKEY',
            }
        })

    def test_repr(self):
        s = repr(self.auth)
        self.assertIn('BasicAuthentication', s)
        self.assertIn('USERNAME', s)


class TestTokenAuthentication(unittest.TestCase):
    def setUp(self):
        self.auth = TokenAuthentication(12345, 'TOKEN')

    def test_attribs(self):
        self.assertEquals(self.auth.user_id, 12345)
        self.assertEquals(self.auth.auth_token, 'TOKEN')

    def test_get_headers(self):
        self.assertEquals(self.auth.get_headers(), {
            'authenticate': {
                'complexType': 'PortalLoginToken',
                'userId': 12345,
                'authToken': 'TOKEN',
            }
        })

    def test_repr(self):
        s = repr(self.auth)
        self.assertIn('TokenAuthentication', s)
        self.assertIn('12345', s)
        self.assertIn('TOKEN', s)