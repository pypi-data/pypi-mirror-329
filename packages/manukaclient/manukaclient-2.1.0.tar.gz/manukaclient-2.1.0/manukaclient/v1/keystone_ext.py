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
from nectarclient_lib import base


class KeystoneExtManager(base.BasicManager):
    base_url = 'v1/keystone-ext'
    resource_class = users.User

    def get_user_by_name(self, user_id):
        # Need to use raw here due to keystone base resource not
        # supporting the resp argument.
        user_raw = self._get(
            f'/{self.base_url}/user-by-name/{user_id}/', return_raw=True
        )
        return self.resource_class(self, user_raw, loaded=True)
