from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from authentication.models import UserProfile  # Replace 'myapp' with your app name

class Command(BaseCommand):
    help = 'Create a user and associate them with a UserProfile'

    def handle(self, *args, **options):
        # Create a user
        user = User.objects.create_user('admin', 'admin123', 'admin123')

        # Create a user profile and associate it with the user
        profile = UserProfile.objects.create(user=user)
        profile.is_admin = True  # Set the 'is_admin' attribute if needed
        profile.save()