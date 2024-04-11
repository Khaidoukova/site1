from django.core.management import BaseCommand
from users.models import User


class Command(BaseCommand):

    # def handle(self, *args, **options):
    #     user = User.objects.create(
    #         email='admin@admin',
    #         first_name='Admin',
    #         last_name='Admin',
    #         is_staff=True,
    #         is_superuser=True,
    #     )
    #
    #     user.set_password('qwerty')
    #     user.save()

    def add_arguments(self, parser):
        parser.add_argument('email', type=str, help='Email of the admin user')
        parser.add_argument('password', type=str, help='New password for the admin user')

    def handle(self, *args, **options):
        email = options['email']
        password = options['password']

        try:
            user = User.objects.get(email=email)
            user.set_password(password)
            user.save()
            self.stdout.write(self.style.SUCCESS(f"Password for admin '{email}' has been successfully updated."))
        except User.DoesNotExist:
            self.stderr.write(self.style.ERROR(f"Admin with email '{email}' does not exist."))