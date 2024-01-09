import asyncio
from io import BytesIO
from typing import Optional
from discord.ext import commands
import discord
from discord import app_commands

import subprocess


def fix_image(
    attachment_bytes: bytes,
) -> Optional[discord.File]:
    try:
        out_bytes = subprocess.check_output(
            input=attachment_bytes, args=["convert", "HEIC:-", "PNG:-"]
        )

        return discord.File(BytesIO(out_bytes), filename="fixed.png")
    except subprocess.CalledProcessError:
        return None


class Image(commands.Cog):
    """The description for BrokenImage goes here."""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.ctx_menu = app_commands.ContextMenu(
            name="fix broken image",
            callback=self.fix_broken_image,
        )
        self.bot.tree.add_command(self.ctx_menu)

    async def cog_unload(self) -> None:
        self.bot.tree.remove_command(self.ctx_menu.name, type=self.ctx_menu.type)

    @app_commands.guilds(559402502102056961, 680401335862296611)
    async def fix_broken_image(
        self, interaction: discord.Interaction, message: discord.Message
    ) -> None:
        await interaction.response.defer()
        await interaction.followup.send(
            file=fix_image(await message.attachments[0].read())
        )


async def setup(bot):
    await bot.add_cog(Image(bot))
