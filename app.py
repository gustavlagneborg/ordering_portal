from project import create_app
import os
import logging

LOG = logging.getLogger(__name__)

# Call the application factory function to construct a Flask application
# instance using the development configuration
os.environ["ENVIROMENT"]="STAGE"
LOG.info(os.environ.get("ENVIROMENT"))
app = create_app(env=os.environ.get("ENVIROMENT"))
