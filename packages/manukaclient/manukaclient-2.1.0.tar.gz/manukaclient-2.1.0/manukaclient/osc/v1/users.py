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

import logging

from nectarclient_lib import exceptions
from osc_lib.command import command
from osc_lib import utils as osc_utils


class ListUsers(command.Lister):
    """List users."""

    log = logging.getLogger(__name__ + '.ListUsers')

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)
        client = self.app.client_manager.account
        users = client.users.list()
        columns = ['id', 'displayname', 'email']
        return (
            columns,
            (osc_utils.get_item_properties(q, columns) for q in users),
        )


class SearchUsers(command.Lister):
    """Search users."""

    log = logging.getLogger(__name__ + '.ListUsers')

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument('query', metavar='<query>', help=('Search query'))
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)
        client = self.app.client_manager.account
        users = client.users.search(parsed_args.query)
        columns = ['id', 'displayname', 'email']
        return (
            columns,
            (osc_utils.get_item_properties(q, columns) for q in users),
        )


class UserCommand(command.ShowOne):
    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument('id', metavar='<id>', help=('ID of user'))
        return parser


class ShowUser(UserCommand):
    """Show user details."""

    log = logging.getLogger(__name__ + '.ShowUser')

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)
        client = self.app.client_manager.account
        try:
            user = client.users.get(parsed_args.id)
        except exceptions.NotFound as ex:
            raise exceptions.CommandError(str(ex))

        return self.dict2columns(user.to_dict())


class UpdateUser(UserCommand):
    """Update an user."""

    log = logging.getLogger(__name__ + '.UpdateUser')

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            '--affiliation', metavar='<affiliation>', help=('Affiliation')
        )
        parser.add_argument(
            '--phone-number', metavar='<phone_number>', help=('phone number')
        )
        parser.add_argument(
            '--mobile-number',
            metavar='<mobile_number>',
            help=('mobile number'),
        )
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)
        client = self.app.client_manager.account
        try:
            user = client.users.get(parsed_args.id)
        except exceptions.NotFound as ex:
            raise exceptions.CommandError(str(ex))

        update = {}
        for field in ['affiliation', 'phone_number', 'mobile_number']:
            if getattr(parsed_args, field):
                update[field] = getattr(parsed_args, field)

        user = client.users.update(parsed_args.id, **update)
        return self.dict2columns(user.to_dict())


class ListPendingUsers(command.Lister):
    """List pending users."""

    log = logging.getLogger(__name__ + '.ListPendingUsers')

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)
        client = self.app.client_manager.account
        users = client.pending_users.list()
        columns = ['id', 'displayname', 'email']
        return (
            columns,
            (osc_utils.get_item_properties(q, columns) for q in users),
        )


class ShowPendingUser(UserCommand):
    """Show pending user details."""

    log = logging.getLogger(__name__ + '.ShowPendingUser')

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)
        client = self.app.client_manager.account
        try:
            user = client.pending_users.get(parsed_args.id)
        except exceptions.NotFound as ex:
            raise exceptions.CommandError(str(ex))

        return self.dict2columns(user.to_dict())


class DeletePendingUser(UserCommand):
    """Delete pending user."""

    log = logging.getLogger(__name__ + '.DeletePendingUser')

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)
        client = self.app.client_manager.account
        try:
            client.pending_users.delete(parsed_args.id)
        except exceptions.NotFound as ex:
            raise exceptions.CommandError(str(ex))
        return [], []
