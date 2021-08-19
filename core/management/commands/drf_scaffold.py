from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Meant to generate Models/Views/Urls/Serializers'

    def add_arguments(self, parser):
        parser.add_argument(
            'app',
            help='app name',
        )

    def handle(self, *args, **kwargs):
        app_name = kwargs['app']
        print(app_name)