from django.core.management import BaseCommand
from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.create(
            email='testdomsaitov123@yandex.ru',
            first_name='SuperAdmin',
            last_name='Admin',
            is_staff=True,
            is_superuser=True,
            is_active=True,
        )

        user.set_password('Kusok0707Kurici2903')
        user.save()
