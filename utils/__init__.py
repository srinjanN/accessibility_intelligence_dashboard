"""
Utils Package Initializer.
Ensures user site-packages directory is on sys.path.
"""

import sys
import os
import site

user_site = site.USER_SITE
if user_site and os.path.exists(user_site) and user_site not in sys.path:
    sys.path.insert(0, user_site)
