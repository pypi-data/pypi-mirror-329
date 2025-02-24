"""signals for helpers"""

# Third Party
from aadiscordbot.tasks import send_message
from discord import Color, Embed

# Django
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

# Alliance Auth
from allianceauth.services.hooks import get_extension_logger

logger = get_extension_logger(__name__)


@receiver(m2m_changed, sender=User)
def m2m_changed_user_groups(instance: User, action, pk_set, **kwargs):
    """
    Trigger welcome message when a user joins a group
    """

    def trigger_welcome_message():
        try:
            logger.debug("Sending welcome message %s", instance)
            # find the groups!

            group_welcome = getattr(instance, "groupwelcome", None)
            if group_welcome:
                channel = group_welcome.channel
                msg = group_welcome.message
                name = instance.name  # Group name

                for user_id in pk_set:  # Loop over users who joined
                    user = User.objects.get(pk=user_id)
                    udid = user.discord.uid  # Get user's Discord ID
                    e = Embed(
                        title=f"**Welcome to {name}**",
                        description=msg,
                        color=Color.green(),
                    )
                    pmsg = f"<@{udid}>"
                    send_message(channel_id=channel, message=pmsg, embed=e)

        except Exception as err:
            logger.error(err)

    if instance.pk and (action == "post_add"):
        transaction.on_commit(trigger_welcome_message)
