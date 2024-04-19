from typing import Literal
from django.core.management.base import BaseCommand
from os import system, name


class Command(BaseCommand):
    help = "Start Celery server"

    def add_arguments(self, parser) -> None:
        parser.add_argument(
            "mode",
            type=str,
            choices=['dev', 'prod'],
            help='Celery server mode',
        )

    def handle(self, *args, **options) -> None:
        mode: Literal['dev', 'prod'] = options["mode"]

        match mode:
            case 'dev':
                system('python -m celery -A core worker -l info -P gevent')

            case 'prod':
                if name == 'nt':
                    message: str = 'Celery cannot run prod in Windows'
                    raise ValueError(message)

                else:
                    system('python -m celery -A core worker')
