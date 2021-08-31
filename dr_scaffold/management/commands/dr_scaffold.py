# pylint: disable=unused-argument
"""
django custom management command class
"""
from django.core.management.base import BaseCommand

from dr_scaffold.generators import Generator


class Command(BaseCommand):
    """
    django custom management command class
    """

    help = """Meant to generate Models, admin, Views, Serializers, Urls files for a ready
     to use REST api"""
    missing_args_message = (
        "You are missing some arguments in your command check the example below"
        "python manage.py dr_scaffold blog Article title:char body:text"
    )

    def add_arguments(self, parser):
        # need to run command as follow: python manage.py dr_scaffold app_name ModelName fields
        parser.add_argument(
            "args",
            metavar="scaffold",
            nargs="*",
            help="""Scaffold arguments (app_name
             ModelName fields).""",
        )
        # Named (optional) arguments
        parser.add_argument(
            "--mixins",
            nargs="?",
            default="None",
            help="ex. --mixins CRUD where CRUD are letters of your viewset actions",
        )

    def handle(self, *args, **kwargs):
        # handle the creation of an app with default files first
        actions = []
        actions[:0] = kwargs["mixins"]
        if kwargs["mixins"] == "None":
            actions = False
        generator = Generator(args[0], args[1], args[2:], actions)
        generator.run()
