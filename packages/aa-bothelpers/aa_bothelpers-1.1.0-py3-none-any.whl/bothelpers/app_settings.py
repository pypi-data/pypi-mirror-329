"""Settings for helpers."""

# Django
from django.apps import apps
from django.conf import settings

# put your app settings here
BOTHELPERS_COGS = getattr(
    settings,
    "BOTHELPERS_COGS",
    [
        "bothelpers.cogs.it",
        "bothelpers.cogs.links",
    ],
)


def securegroups_active():
    """
    Check if securegroups is installed
    """
    return apps.is_installed("securegroups")
