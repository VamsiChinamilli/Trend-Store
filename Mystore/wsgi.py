import os
import sys
from django.core.wsgi import get_wsgi_application

# 1. Get the absolute path of the directory containing wsgi.py
# (This is your inner 'Mystore' folder)
current_dir = os.path.dirname(os.path.abspath(__file__))

# 2. Get the path of the parent directory (the root where manage.py lives)
project_root = os.path.dirname(current_dir)

# 3. Add both to the system path so Django can 'see' itself
if project_root not in sys.path:
    sys.path.append(project_root)
if current_dir not in sys.path:
    sys.path.append(current_dir)

# 4. Point to your settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Mystore.settings')

application = get_wsgi_application()
app = application  # Critical for Vercel