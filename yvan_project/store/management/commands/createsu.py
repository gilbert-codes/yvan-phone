from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Create a superuser automatically'

    def handle(self, *args, **options):
        username = 'yvan'
        email = 'yvan@example.com'
        password = 'yvan123'
        
        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            self.stdout.write(self.style.SUCCESS(f'✅ Superuser "{username}" created!'))
            self.stdout.write(self.style.SUCCESS(f'   Password: {password}'))
        else:
            self.stdout.write(self.style.WARNING(f'⚠️ Superuser "{username}" already exists!'))