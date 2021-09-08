
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
import django
django.setup()

from users.models import User

if __name__ == "__main__":
    
    superuser = User.objects.create_superuser(
        username='admin', email='admin@admin.com', password='admin'
    )
    