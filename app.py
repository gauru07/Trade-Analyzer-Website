# This file is created as a fallback for Render.com deployment
# The actual Django application is in finance_analyzer.wsgi:application

import os
import sys
from django.core.wsgi import get_wsgi_application

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'finance_analyzer.settings')

# Get the WSGI application
application = get_wsgi_application()

# This allows Render.com to find the app if it's looking for app:app
app = application
