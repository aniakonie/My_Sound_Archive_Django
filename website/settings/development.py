import os
from dotenv import load_dotenv
import dj_database_url

from website.settings.base import *

load_dotenv()

database_url = os.getenv('DATABASE_URL')
DATABASES['default'] = dj_database_url.parse(database_url)
