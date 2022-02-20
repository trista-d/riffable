# Entry point for the application.
from . import app    # For application discovery by the 'flask' command.
from . import views  # For import side-effects of setting up routes.

# to set environment variable in powershell
# $env:FLASK_APP = "name_of_this_file"