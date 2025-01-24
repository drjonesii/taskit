from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from tasks.models import Category

class Command(BaseCommand):
    help = 'Seed the database with initial data'

    def handle(self, *args, **kwargs):
        # Create admin user
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'adminpass')
            self.stdout.write(self.style.SUCCESS('Admin user created'))

        # Create categories
        categories = ['tech debt', 'enhancement', 'fun stuff', 'stretch', 'personal']
        for category_name in categories:
            if not Category.objects.filter(name=category_name).exists():
                Category.objects.create(name=category_name)
                self.stdout.write(self.style.SUCCESS(f'Category "{category_name}" created'))

        self.stdout.write(self.style.SUCCESS('Database seeded successfully'))
