"""App Configuration"""

# Django
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

# Bot Helpers
# Alt Corp
from bothelpers import __version__


class ExampleConfig(AppConfig):
    """App Config"""

    name = "bothelpers"
    label = "bothelpers"
    verbose_name = _(f"Bot Helpers v{__version__}")

    def ready(self):
        # bot helpers
        # Alt Corp
        # Bot Helpers
        import bothelpers.signals  # noqa: F401
