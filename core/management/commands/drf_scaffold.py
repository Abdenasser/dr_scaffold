from django.core.management.base import BaseCommand
from core.generators import Generator

class Command(BaseCommand):
    help = 'Meant to generate Models/Views/Urls/Serializers'
    missing_args_message = (
        "You are missing some arguments in your command check the example below"
        "python manage.py drf_scaffold blog Article title:char body:text"
    )

    def add_arguments(self, parser):
        #need to run command as follow: python manage.py drf_scaffold app_name ModelName fields
        parser.add_argument(
            'args', metavar='scaffold', nargs='*', help='Scaffold arguments (app_name ModelName fields).'
        )

    def handle(self, *args, **kwargs):
        # handle the creation of an app with default files first
        generator = Generator(args[0], args[1], args[2:]) 
        generator.generate()