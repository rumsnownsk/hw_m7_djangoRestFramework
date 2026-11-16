# core/management/commands/init_data.py

from django.core.management.base import BaseCommand
from django.core.management import call_command

from users.models import Payment
from lms.models import Course, Lesson
from django.contrib.auth import get_user_model


User = get_user_model()

MODELS_TO_CHECK = {
    'Пользователи': User,
    'Курсы': Course,
    'Уроки': Lesson,
    'Платежи': Payment,
}

class Command(BaseCommand):
    help = 'Загружает демо-данные из фикстуры'

    def add_arguments(self, parser):
        parser.add_argument(
            '-y', '--yes',
            action='store_true',
            help='Не спрашивать подтверждение',
        )

    def handle(self, *args, **options):
        filled = [name for name, model in MODELS_TO_CHECK.items() if model.objects.exists()]

        if not filled:
            # База пустая по всем моделям — грузим без вопросов о дубликатах
            call_command('loaddata', 'core/data/fixtures_full', verbosity=1)
            self.stdout.write(self.style.SUCCESS('Демо-данные загружены'))
            return

        if len(filled) < len(MODELS_TO_CHECK):
            missing = [name for name in MODELS_TO_CHECK if name not in filled]
            self.stdout.write(self.style.WARNING(
                f'Частично заполненная база. Есть: {", ".join(filled)}. '
                f'Отсутствуют: {", ".join(missing)}.'
            ))
        else:
            self.stdout.write(self.style.WARNING(
                'Все таблицы уже заполнены демо-данными.'
            ))

        if not options['yes']:
            answer = input(
                'Продолжить загрузку? Существующие записи с теми же id будут '
                'перезаписаны, отсутствующие — созданы. [y/N]: '
            )
            if answer.strip().lower() not in ('y', 'yes', 'д', 'да'):
                self.stdout.write('Отменено. База без изменений.')
                return

        call_command('loaddata', 'core/data/fixtures_full', verbosity=1)
        self.stdout.write(self.style.SUCCESS('Загрузка завершена'))