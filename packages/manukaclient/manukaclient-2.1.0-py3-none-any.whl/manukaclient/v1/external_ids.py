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


class ExternalId(base.Resource):
    date_fields = ['last_login']

    def __repr__(self):
        return f"<ExternalId {self.id}>"


class ExternalIdManager(base.Manager):
    base_url = 'v1/external-ids'
    resource_class = ExternalId

    def update(self, external_id, **kwargs):
        return self._update(f'/{self.base_url}/{external_id}/', data=kwargs)

    def delete(self, external_id):
        return self._delete(f'/{self.base_url}/{external_id}/')
