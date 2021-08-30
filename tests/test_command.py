"""
Tests for management command
"""
from unittest import mock

import django
from django.core.management import call_command
from django.test import override_settings
from django.test.testcases import SimpleTestCase

django.setup()


@override_settings(
    INSTALLED_APPS=[
        "dr_scaffold",
    ],
)
class CommandTestCase(SimpleTestCase):
    """
    simple tests for management command
    """

    @classmethod
    @mock.patch("dr_scaffold.generators.Generator.run")
    def test_command(cls, mock_run):
        """
        Test for successful command call
        """
        call_command("dr_scaffold", "blog", "Article", "title:charfield", False)
        mock_run.assert_called()

    @classmethod
    @mock.patch("dr_scaffold.generators.Generator.generate")
    def test_generate_api(cls, mock_generate_api):
        """
        Test for successful command call
        """
        call_command("dr_scaffold", "blog", "Article", "title:charfield", False)
        mock_generate_api.assert_called()
