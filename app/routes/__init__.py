# Finds module named "home" in the current directory.
#imports the bp obect, rename it as home
from .home import bp as home

from .api import bp as api

# Import dashboard routes as dashboard
from .dashboard import bp as dashboard