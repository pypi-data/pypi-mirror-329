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

from nectarclient_lib import base

from manukaclient.v1 import external_ids


class User(base.Resource):
    date_fields = ['registered_at', 'terms_accepted_at', 'last_login']

    def __init__(self, manager, info, loaded=False, resp=None):
        super().__init__(manager, info, loaded, resp)
        raw_external_ids = getattr(self, 'external_ids', [])
        self.external_ids = []
        for eid in raw_external_ids:
            self.external_ids.append(external_ids.ExternalId(manager, eid))

    def __repr__(self):
        return f"<User {self.id}>"


class UserManager(base.BasicManager):
    base_url = 'v1/users'
    resource_class = User

    def update(self, user_id, **kwargs):
        return self._update(f'/{self.base_url}/{user_id}/', data=kwargs)

    def projects(self, user_id, role_name):
        return self._get(
            f'/{self.base_url}/{user_id}/projects/{role_name}/',
            return_raw=True,
        )

    def search(self, query):
        return self._search(
            f'/{self.base_url}/search/', data={'search': query}
        )


class PendingUserManager(UserManager):
    base_url = 'v1/pending-users'

    def delete(self, user_id):
        return self._delete(f'/{self.base_url}/{user_id}/')
