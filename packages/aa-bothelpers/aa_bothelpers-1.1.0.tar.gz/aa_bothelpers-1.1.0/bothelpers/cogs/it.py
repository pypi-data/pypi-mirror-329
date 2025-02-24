"""
IT Commands
"""

# Standard Library
import asyncio

# Third Party
from aadiscordbot.app_settings import get_all_servers
from aadiscordbot.cogs.utils.decorators import sender_has_perm
from discord import AutocompleteContext
from discord.commands import SlashCommandGroup, option
from discord.ext import commands

# Django
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

# Alliance Auth
from allianceauth.eveonline.models import EveCharacter
from allianceauth.eveonline.tasks import update_character
from allianceauth.services.hooks import get_extension_logger

# Bot Helpers
from bothelpers.app_settings import securegroups_active

logger = get_extension_logger(__name__)


class IT(commands.Cog):
    """
    IT Commands
    """

    def __init__(self, bot):
        self.bot = bot

    it_commands = SlashCommandGroup("it", "IT Commands", guild_ids=get_all_servers())

    async def search_characters(self, ctx: AutocompleteContext):
        """Returns a list of toons that begin with the characters entered so far."""
        return list(
            EveCharacter.objects.filter(
                character_name__icontains=ctx.value
            ).values_list("character_name", flat=True)[:10]
        )

    # Sets up slash command for syncing all data of user
    @it_commands.command(
        name="update_user",
        description="updates user",
        guild_ids=[int(settings.DISCORD_GUILD_ID)],
    )
    @sender_has_perm("bothelpers.it_commands")
    @option(
        "character",
        description="Search for a Character!",
        autocomplete=search_characters,
    )
    async def update_user(self, ctx, character: str):
        """
        Queue Update tasks for the character and all alts. Run compliant group
        """
        try:
            char = EveCharacter.objects.get(character_name=character)
            alts = (
                char.character_ownership.user.character_ownerships.all()
                .select_related("character")
                .values_list("character__character_id", flat=True)
            )
            for c in alts:
                update_character.delay(c)
            await ctx.respond(
                f"Sent tasks to update **{character}**'s Alts", ephemeral=True
            )
        except EveCharacter.DoesNotExist:
            return await ctx.respond(
                f"Character **{character}** does not exist in our Auth system",
                ephemeral=True,
            )
        except ObjectDoesNotExist:
            return await ctx.respond(
                f"**{character}** is Unlinked unable to update characters",
                ephemeral=True,
            )

        if securegroups_active():
            # Third Party
            from securegroups.tasks import (  # pylint: disable=import-error
                run_smart_groups,
            )

            await asyncio.sleep(30)
            try:
                run_smart_groups()
                await ctx.respond("Sent task to update secure groups", ephemeral=True)
            except Exception:
                return await ctx.respond("secure group update failed", ephemeral=True)


def setup(bot):
    """Load the cog"""
    bot.add_cog(IT(bot))
