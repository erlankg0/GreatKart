from django.core.management.base import BaseCommand
from accounts.models import Account


# Command for create superuser
class Command(BaseCommand):
    help = 'Create superuser'  # help for command

    def handle(self, *args, **options):  # handle command
        username = 'erlan'  # username
        email = 'era.ab.02@gmail.com'  # email
        phone = '+905555555555'  # phone
        password = '123321era'  # password
        user = Account.objects.create_superuser(
            username=username,
            email=email,
            phone=phone,
            password=password
        )  # create superuser
        user.save()  # save superuser
        print('Superuser created')  # print message
