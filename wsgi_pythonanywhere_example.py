# Copy this entire file into your PythonAnywhere WSGI configuration file.
# Replace YOUR_PA_USERNAME with your PythonAnywhere username.

import os
import sys

path = "/home/YOUR_PA_USERNAME/GlasgowSurvivalGuide"
if path not in sys.path:
    sys.path.insert(0, path)

from dotenv import load_dotenv
load_dotenv(os.path.join(path, ".env"))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "GlasgowSurvivalGuide.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
