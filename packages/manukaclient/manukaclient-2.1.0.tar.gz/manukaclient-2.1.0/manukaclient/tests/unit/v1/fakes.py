#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import re
from unittest import mock
from urllib import parse

from nectarclient_lib.tests.unit import fakes
from nectarclient_lib.tests.unit import utils

from manukaclient import client as base_client
from manukaclient.v1 import client
from manukaclient.v1 import external_ids
from manukaclient.v1 import keystone_ext
from manukaclient.v1 import users


# regex to compare callback to result of get_endpoint()
# checks version number (vX or vX.X where X is a number)
# and also checks if the id is on the end
ENDPOINT_RE = re.compile(r"^get_http:__manuka_api:8774_v\d(_\d)?_\w{32}$")

# accepts formats like v2 or v2.1
ENDPOINT_TYPE_RE = re.compile(r"^v\d(\.\d)?$")

# accepts formats like v2 or v2_1
CALLBACK_RE = re.compile(r"^get_http:__manuka_api:8774_v\d(_\d)?$")

generic_user = {
    "first_name": "uEelNrtNg3SPzh50nol5",
    "affiliation": "staff",
    "id": 123,
    "home_organization": "saDjCIriNGoJKqUI4piX",
    "mobile_number": "6Q1llL0jyOhNdyBAX0XO",
    "terms_accepted_at": "2015-10-21T15:18:40",
    "surname": "OIEBQswE3tNh89N5OTsW",
    "user_id": "d1fa8867e42444cf8724e65fef1da549",
    "phone_number": "33443322",
    "displayname": "lyWtLuxXWxku24cbhgjT",
    "registered_at": "2015-10-21T15:18:40",
    "email": "fmklmf4ikmlf34mnm",
    "ignore_username_not_email": False,
    "orcid": "sammmee",
    "state": "created",
    "last_login": "2020-04-23T10:23:20",
    "terms_version": "v1",
    "external_ids": [
        {
            "id": 1233,
            "last_login": "2020-04-23T10:23:20",
            "idp": "https://idp/idp/shibboleth",
        }
    ],
}


class FakeClient(fakes.FakeClient, client.Client):
    def __init__(self, *args, **kwargs):
        client.Client.__init__(self, session=mock.Mock())
        self.http_client = FakeSessionClient(**kwargs)
        self.users = users.UserManager(self.http_client)
        self.pending_users = users.PendingUserManager(self.http_client)
        self.external_ids = external_ids.ExternalIdManager(self.http_client)
        self.keystone_ext = keystone_ext.KeystoneExtManager(self.http_client)


class FakeSessionClient(base_client.SessionClient):
    def __init__(self, *args, **kwargs):
        self.callstack = []
        self.visited = []
        self.auth = mock.Mock()
        self.session = mock.Mock()
        self.service_type = 'service_type'
        self.service_name = None
        self.endpoint_override = None
        self.interface = None
        self.region_name = None
        self.version = None
        self.auth.get_auth_ref.return_value.project_id = 'tenant_id'
        # determines which endpoint to return in get_endpoint()
        # NOTE(augustina): this is a hacky workaround, ultimately
        # we need to fix our whole mocking architecture (fixtures?)
        if 'endpoint_type' in kwargs:
            self.endpoint_type = kwargs['endpoint_type']
        else:
            self.endpoint_type = 'endpoint_type'
        self.logger = mock.MagicMock()

    def request(self, url, method, **kwargs):
        return self._cs_request(url, method, **kwargs)

    def _cs_request(self, url, method, **kwargs):
        # Check that certain things are called correctly
        if method in ['GET', 'DELETE']:
            assert 'data' not in kwargs
        elif method == 'PUT':
            assert 'data' in kwargs

        if url is not None:
            # Call the method
            args = parse.parse_qsl(parse.urlparse(url)[4])
            kwargs.update(args)
            munged_url = url.rsplit('?', 1)[0]
            munged_url = munged_url.strip('/').replace('/', '_')
            munged_url = munged_url.replace('.', '_')
            munged_url = munged_url.replace('-', '_')
            munged_url = munged_url.replace(' ', '_')
            munged_url = munged_url.replace('!', '_')
            munged_url = munged_url.replace('@', '_')
            munged_url = munged_url.replace('%20', '_')
            munged_url = munged_url.replace('%3A', '_')
            callback = f"{method.lower()}_{munged_url}"

        if not hasattr(self, callback):
            raise AssertionError(
                f'Called unknown API method: {method} {url}, '
                f'expected fakes method name: {callback}'
            )

        # Note the call
        self.visited.append(callback)
        self.callstack.append(
            (method, url, kwargs.get('data'), kwargs.get('params'))
        )

        status, headers, data = getattr(self, callback)(**kwargs)

        r = utils.TestResponse(
            {
                "status_code": status,
                "text": data,
                "headers": headers,
            }
        )
        return r, data

    def get_v1_users(self, **kw):
        users = [
            {
                "first_name": "uEelNrtNg3SPzh50nol5",
                "affiliation": "staff",
                "id": 123,
                "home_organization": "saDjCIriNGoJKqUI4piX",
                "mobile_number": "6Q1llL0jyOhNdyBAX0XO",
                "terms_accepted_at": "2015-10-21T15:18:40",
                "surname": "OIEBQswE3tNh89N5OTsW",
                "user_id": "d1fa8867e42444cf8724e65fef1da549",
                "phone_number": "33443322",
                "displayname": "lyWtLuxXWxku24cbhgjT",
                "registered_at": "2015-10-21T15:18:40",
                "email": "fmklmf4ikmlf34mnm",
                "ignore_username_not_email": False,
                "orcid": "sammmee",
                "state": "created",
                "last_login": "2020-04-23T10:23:20",
                "terms_version": "v1",
            },
            {
                "first_name": "uEelNrtNg3SPzh50nol5",
                "affiliation": "staff",
                "id": 124,
                "home_organization": "saDjCIriNGoJKqUI4piX",
                "mobile_number": "6Q1llL0jyOhNdyBAX0XO",
                "terms_accepted_at": "2015-10-21T15:18:40",
                "surname": "OIEBQswE3tNh89N5OTsW",
                "user_id": "d1fa8867e42444cf8724e65fef1da549",
                "phone_number": "33443322",
                "displayname": "lyWtLuxXWxku24cbhgjT",
                "registered_at": "2015-10-21T15:18:40",
                "email": "fmklmf4ikmlf34mnm",
                "ignore_username_not_email": False,
                "orcid": "sammmee",
                "state": "created",
                "last_login": "2020-04-23T10:23:20",
                "terms_version": "v1",
            },
            {
                "first_name": "uEelNrtNg3SPzh50nol5",
                "affiliation": "staff",
                "id": 125,
                "home_organization": "saDjCIriNGoJKqUI4piX",
                "mobile_number": "6Q1llL0jyOhNdyBAX0XO",
                "terms_accepted_at": "2015-10-21T15:18:40",
                "surname": "OIEBQswE3tNh89N5OTsW",
                "user_id": "d1fa8867e42444cf8724e65fef1da549",
                "phone_number": "33443322",
                "displayname": "lyWtLuxXWxku24cbhgjT",
                "registered_at": "2015-10-21T15:18:40",
                "email": "fmklmf4ikmlf34mnm",
                "ignore_username_not_email": False,
                "orcid": "sammmee",
                "state": "created",
                "last_login": "2020-04-23T10:23:20",
                "terms_version": "v1",
            },
        ]
        return (200, {}, users)

    def get_v1_users_123(self, **kw):
        return (200, {}, generic_user)

    def patch_v1_users_123(self, data, **kw):
        return (
            202,
            {'phone_number': 'new-phone_number'},
            {
                "first_name": "uEelNrtNg3SPzh50nol5",
                "affiliation": "staff",
                "id": 123,
                "home_organization": "saDjCIriNGoJKqUI4piX",
                "mobile_number": "6Q1llL0jyOhNdyBAX0XO",
                "terms_accepted_at": "2015-10-21T15:18:40",
                "surname": "OIEBQswE3tNh89N5OTsW",
                "user_id": "d1fa8867e42444cf8724e65fef1da549",
                "phone_number": "new-phone_number",
                "displayname": "lyWtLuxXWxku24cbhgjT",
                "registered_at": "2015-10-21T15:18:40",
                "email": "fmklmf4ikmlf34mnm",
                "ignore_username_not_email": False,
                "orcid": "new-orcid",
                "state": "created",
                "last_login": "2020-04-23T10:23:20",
                "terms_version": "v1",
            },
        )

    def get_v1_users_123_projects_3456(self, **kw):
        return (200, {}, ['01234567890123456789', '98765432109876543210'])

    def post_v1_users_search(self, data, **kw):
        users = [
            {
                "first_name": "uEelNrtNg3SPzh50nol5",
                "affiliation": "staff",
                "id": 123,
                "home_organization": "saDjCIriNGoJKqUI4piX",
                "mobile_number": "6Q1llL0jyOhNdyBAX0XO",
                "terms_accepted_at": "2015-10-21T15:18:40",
                "surname": "OIEBQswE3tNh89N5OTsW",
                "user_id": "d1fa8867e42444cf8724e65fef1da549",
                "phone_number": "33443322",
                "displayname": "lyWtLuxXWxku24cbhgjT",
                "registered_at": "2015-10-21T15:18:40",
                "email": "fmklmf4ikmlf34mnm",
                "ignore_username_not_email": False,
                "orcid": "sammmee",
                "state": "created",
                "last_login": "2020-04-23T10:23:20",
                "terms_version": "v1",
            },
            {
                "first_name": "uEelNrtNg3SPzh50nol5",
                "affiliation": "staff",
                "id": 124,
                "home_organization": "saDjCIriNGoJKqUI4piX",
                "mobile_number": "6Q1llL0jyOhNdyBAX0XO",
                "terms_accepted_at": "2015-10-21T15:18:40",
                "surname": "OIEBQswE3tNh89N5OTsW",
                "user_id": "d1fa8867e42444cf8724e65fef1da549",
                "phone_number": "33443322",
                "displayname": "lyWtLuxXWxku24cbhgjT",
                "registered_at": "2015-10-21T15:18:40",
                "email": "fmklmf4ikmlf34mnm",
                "ignore_username_not_email": False,
                "orcid": "sammmee",
                "state": "created",
                "last_login": "2020-04-23T10:23:20",
                "terms_version": "v1",
            },
            {
                "first_name": "uEelNrtNg3SPzh50nol5",
                "affiliation": "staff",
                "id": 125,
                "home_organization": "saDjCIriNGoJKqUI4piX",
                "mobile_number": "6Q1llL0jyOhNdyBAX0XO",
                "terms_accepted_at": "2015-10-21T15:18:40",
                "surname": "OIEBQswE3tNh89N5OTsW",
                "user_id": "d1fa8867e42444cf8724e65fef1da549",
                "phone_number": "33443322",
                "displayname": "lyWtLuxXWxku24cbhgjT",
                "registered_at": "2015-10-21T15:18:40",
                "email": "fmklmf4ikmlf34mnm",
                "ignore_username_not_email": False,
                "orcid": "sammmee",
                "state": "created",
                "last_login": "2020-04-23T10:23:20",
                "terms_version": "v1",
            },
        ]

        return (200, {}, users)

    def get_v1_pending_users(self, **kw):
        users = [
            {
                "first_name": "uEelNrtNg3SPzh50nol5",
                "affiliation": "staff",
                "id": 123,
                "home_organization": "saDjCIriNGoJKqUI4piX",
                "mobile_number": "6Q1llL0jyOhNdyBAX0XO",
                "terms_accepted_at": "2015-10-21T15:18:40",
                "surname": "OIEBQswE3tNh89N5OTsW",
                "user_id": "d1fa8867e42444cf8724e65fef1da549",
                "phone_number": "33443322",
                "displayname": "lyWtLuxXWxku24cbhgjT",
                "registered_at": "2015-10-21T15:18:40",
                "email": "fmklmf4ikmlf34mnm",
                "ignore_username_not_email": False,
                "orcid": "sammmee",
                "state": "created",
                "last_login": "2020-04-23T10:23:20",
                "terms_version": "v1",
            },
            {
                "first_name": "uEelNrtNg3SPzh50nol5",
                "affiliation": "staff",
                "id": 124,
                "home_organization": "saDjCIriNGoJKqUI4piX",
                "mobile_number": "6Q1llL0jyOhNdyBAX0XO",
                "terms_accepted_at": "2015-10-21T15:18:40",
                "surname": "OIEBQswE3tNh89N5OTsW",
                "user_id": "d1fa8867e42444cf8724e65fef1da549",
                "phone_number": "33443322",
                "displayname": "lyWtLuxXWxku24cbhgjT",
                "registered_at": "2015-10-21T15:18:40",
                "email": "fmklmf4ikmlf34mnm",
                "ignore_username_not_email": False,
                "orcid": "sammmee",
                "state": "created",
                "last_login": "2020-04-23T10:23:20",
                "terms_version": "v1",
            },
            {
                "first_name": "uEelNrtNg3SPzh50nol5",
                "affiliation": "staff",
                "id": 125,
                "home_organization": "saDjCIriNGoJKqUI4piX",
                "mobile_number": "6Q1llL0jyOhNdyBAX0XO",
                "terms_accepted_at": "2015-10-21T15:18:40",
                "surname": "OIEBQswE3tNh89N5OTsW",
                "user_id": "d1fa8867e42444cf8724e65fef1da549",
                "phone_number": "33443322",
                "displayname": "lyWtLuxXWxku24cbhgjT",
                "registered_at": "2015-10-21T15:18:40",
                "email": "fmklmf4ikmlf34mnm",
                "ignore_username_not_email": False,
                "orcid": "sammmee",
                "state": "created",
                "last_login": "2020-04-23T10:23:20",
                "terms_version": "v1",
            },
        ]
        return (200, {}, users)

    def delete_v1_pending_users_123(self, **kw):
        return (204, {}, {})

    def get_v1_pending_users_123(self, **kw):
        return (200, {}, generic_user)

    def delete_v1_external_ids_123(self, **kw):
        return (204, {}, {})

    def patch_v1_external_ids_123(self, data, **kw):
        return (
            202,
            {},
            {
                "id": 134,
                "last_login": "2020-04-23T10:23:20",
                "idp": "F72fIjesixhkTUSzMxdF",
            },
        )

    def get_v1_keystone_ext_user_by_name_bob(self, **kw):
        ks_user = {
            'email': 'email@example.com',
            'full_name': 'displayName-lyWtLuxXWxku24cbhgjT',
            'inactive': False,
            'id': '123456789',
            'name': 'email@example.com',
            'domain_id': 'default',
            'enabled': True,
            'default_project_id': '987654321',
            'password_expires_at': None,
            'options': {},
            'links': {'self': 'http://keystone:5000/v3/users/123456789'},
        }
        return (200, {}, ks_user)
