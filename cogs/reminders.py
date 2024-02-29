from discord.ext import commands
import discord

class Reminders(commands.Cog):
    """The description for Reminders goes here."""

    def __init__(self, bot):
        self.bot = bot

async def setup(bot):
    await bot.add_cog(Reminders(bot))
