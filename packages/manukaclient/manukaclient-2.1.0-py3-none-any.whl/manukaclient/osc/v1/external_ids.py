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


class ExternalIdCommand(command.ShowOne):
    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument('id', metavar='<id>', help=('ID of external_id'))
        return parser


class ShowExternalId(ExternalIdCommand):
    """Show external id details."""

    log = logging.getLogger(__name__ + '.ShowExternalId')

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)
        client = self.app.client_manager.account
        try:
            external_id = client.external_ids.get(parsed_args.id)
        except exceptions.NotFound as ex:
            raise exceptions.CommandError(str(ex))

        return self.dict2columns(external_id.to_dict())


class DeleteExternalId(ExternalIdCommand):
    """Delete external id."""

    log = logging.getLogger(__name__ + '.DeleteExternalId')

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)
        client = self.app.client_manager.account
        try:
            client.external_ids.delete(parsed_args.id)
        except exceptions.NotFound as ex:
            raise exceptions.CommandError(str(ex))

        return [], []


class UpdateExternalId(ExternalIdCommand):
    """Update an external id."""

    log = logging.getLogger(__name__ + '.UpdateExternalId')

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            '--user-id', metavar='<user_id>', help=('User ID of external ID')
        )
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)
        client = self.app.client_manager.account
        try:
            client.external_ids.update(
                parsed_args.id, user_id=parsed_args.user_id
            )
        except exceptions.NotFound as ex:
            raise exceptions.CommandError(str(ex))

        # Return the user as more useful
        user = client.users.get(parsed_args.user_id)

        return self.dict2columns(user.to_dict())
