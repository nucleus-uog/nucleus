import os
from channels.asgi import get_channel_layer

# Use the production settings for asgi.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nucleus.production_settings")

channel_layer = get_channel_layer()
