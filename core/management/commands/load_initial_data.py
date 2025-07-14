from django.core.management.base import BaseCommand
from core.models import Category

class Command(BaseCommand):
    help = 'Ładuje początkowe dane do bazy'

    def handle(self, *args, **kwargs):
        categories = [
            {'name': 'Ubrania', 'icon': '👕'},
            {'name': 'Elektronika', 'icon': '📱'},
            {'name': 'Kosmetyki', 'icon': '🧴'},
            {'name': 'Dokumenty', 'icon': '📄'},
            {'name': 'Leki', 'icon': '💊'},
            {'name': 'Jedzenie', 'icon': '🍎'},
            {'name': 'Sport', 'icon': '⚽'},
            {'name': 'Inne', 'icon': '📦'},
        ]

        for category_data in categories:
            Category.objects.get_or_create(
                name=category_data['name'],
                defaults={'icon': category_data['icon']}
            )
            self.stdout.write(
                self.style.SUCCESS(f'Utworzono kategorię: {category_data["name"]}')
            ) 