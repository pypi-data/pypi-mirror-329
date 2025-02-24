#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.
#

import datetime
import json

from nectarclient_lib.tests.unit import utils

from manukaclient.tests.unit.v1 import fakes
from manukaclient.v1 import users


class UsersTest(utils.TestCase):
    def setUp(self):
        super().setUp()
        self.cs = fakes.FakeClient()

    def test_user_list(self):
        ul = self.cs.users.list()
        self.cs.assert_called('GET', '/v1/users/')
        for u in ul:
            self.assertIsInstance(u, users.User)
        self.assertEqual(3, len(ul))

    def test_user_get(self):
        u = self.cs.users.get(123)
        self.cs.assert_called('GET', '/v1/users/123/')
        self.assertIsInstance(u, users.User)
        self.assertEqual(123, u.id)
        self.assertIsInstance(u.registered_at, datetime.datetime)
        self.assertIsInstance(u.terms_accepted_at, datetime.datetime)

    def test_user_projects(self):
        r = self.cs.users.projects(123, 3456)
        self.cs.assert_called('GET', '/v1/users/123/projects/3456/')
        self.assertEqual(2, len(r))
        self.assertEqual('01234567890123456789', r[0])
        self.assertEqual('98765432109876543210', r[1])

    def test_update(self):
        new_phone_number = 'new-phone_number'
        u = self.cs.users.update(123, phone_number=new_phone_number)
        self.cs.assert_called(
            'PATCH',
            '/v1/users/123/',
            json.dumps({'phone_number': new_phone_number}),
        )
        self.assertIsInstance(u, users.User)
        self.assertEqual(new_phone_number, u.phone_number)

    def test_search(self):
        query = 'needle'
        ul = self.cs.users.search(query)
        self.cs.assert_called(
            'POST', '/v1/users/search/', json.dumps({'search': query})
        )
        for u in ul:
            self.assertIsInstance(u, users.User)


class PendingUsersTest(utils.TestCase):
    def setUp(self):
        super().setUp()
        self.cs = fakes.FakeClient()

    def test_user_list(self):
        ul = self.cs.pending_users.list()
        self.cs.assert_called('GET', '/v1/pending-users/')
        for u in ul:
            self.assertIsInstance(u, users.User)
        self.assertEqual(3, len(ul))

    def test_user_get(self):
        u = self.cs.pending_users.get(123)
        self.cs.assert_called('GET', '/v1/pending-users/123/')
        self.assertIsInstance(u, users.User)
        self.assertEqual(123, u.id)

    def test_user_delete(self):
        self.cs.pending_users.delete(123)
        self.cs.assert_called('DELETE', '/v1/pending-users/123/')
