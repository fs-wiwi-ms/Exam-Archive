import os

from dotenv import load_dotenv

from examarchive.settings.common import *  # noqa: F403

# Load the .env file
load_dotenv()

# Load execution mode settings
if os.environ.get("DJANGO_ENV", "development") == "development":
    from examarchive.settings.development import *  # noqa: F403
else:
    from examarchive.settings.production import *  # noqa: F403
