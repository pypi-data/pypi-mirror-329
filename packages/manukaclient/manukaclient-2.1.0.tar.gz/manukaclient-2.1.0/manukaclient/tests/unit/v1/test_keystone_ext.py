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

from keystoneclient.v3 import users
from nectarclient_lib.tests.unit import utils

from manukaclient.tests.unit.v1 import fakes


class KeystoneTest(utils.TestCase):
    def setUp(self):
        super().setUp()
        self.cs = fakes.FakeClient()

    def test_get_user_by_name(self):
        u = self.cs.keystone_ext.get_user_by_name('bob')
        self.cs.assert_called('GET', '/v1/keystone-ext/user-by-name/bob/')
        self.assertIsInstance(u, users.User)
        self.assertEqual('123456789', u.id)
