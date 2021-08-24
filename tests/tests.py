

import django
from django.conf import settings
from django.core.management import call_command
from django.test import override_settings
from django.test.testcases import SimpleTestCase
from dr_scaffold.generators import Generator
from unittest import mock

settings.configure()
django.setup()

@override_settings(
    INSTALLED_APPS=[
        'dr_scaffold',
    ],
)

class CommandTestCase(SimpleTestCase):
    @mock.patch('dr_scaffold.management.commands.dr_scaffold.Command.add_arguments')
    def test_add_arguments(self, mock_add_arguments):
        call_command('dr_scaffold', 'blog', 'Article', 'title:charfield')
        mock_add_arguments.assert_called()

    @mock.patch('dr_scaffold.management.commands.dr_scaffold.Command.handle')
    def test_add_arguments(self, mock_handle):
        call_command('dr_scaffold', 'blog', 'Article', 'title:charfield')
        mock_handle.assert_called()

    @mock.patch('dr_scaffold.generators.Generator.run')
    def test_command(self, mock_run):
        call_command('dr_scaffold', 'blog', 'Article', 'title:charfield')
        mock_run.assert_called()

    @mock.patch('dr_scaffold.generators.Generator.generate_app')
    def test_generate_api(self, mock_generate_api):
        call_command('dr_scaffold', 'blog', 'Article', 'title:charfield')
        mock_generate_api.assert_called()