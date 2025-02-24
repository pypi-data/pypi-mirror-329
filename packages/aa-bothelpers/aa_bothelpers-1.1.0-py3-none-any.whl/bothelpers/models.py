"""
App Models
Create your models in here
"""

# Django
from django.contrib.auth.models import Group
from django.db import models
from django.utils.translation import gettext_lazy as _


class General(models.Model):
    """Meta model for app permissions"""

    class Meta:
        """Meta definitions"""

        managed = False
        default_permissions = ()
        permissions = (("it_commands", _("Can use IT commands")),)


class Link(models.Model):
    """Link model"""

    class LinkType(models.TextChoices):
        """Link types"""

        GENERAL = "GENERAL", "General Link"
        AUTH = "AUTH", "Alliance Auth Link"
        INTEL = "INTEL", "Intel Link"

    type = models.CharField(
        max_length=20,
        choices=LinkType.choices,
        default=LinkType.GENERAL,
        help_text="Type of link",
    )
    description = models.TextField(
        max_length=500, help_text="Description of what this link is"
    )
    name = models.CharField(
        max_length=255,
        null=False,
        unique=True,
        help_text="A simple name to find this link",
    )
    url = models.CharField(max_length=255, null=False)
    thumbnail = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = "Link"
        verbose_name_plural = "Links"

    def __str__(self):
        return self.name


class GroupWelcome(models.Model):
    """Group Welcome Message"""

    group = models.OneToOneField(Group, on_delete=models.CASCADE)
    message = models.TextField()
    enabled = models.BooleanField(default=True)
    channel = models.BigIntegerField()

    class Meta:
        verbose_name = "Group Welcome Message"
        verbose_name_plural = "Group Welcome Messages"

    def __str__(self):
        return f"Welcome Message: {self.group.name}"
