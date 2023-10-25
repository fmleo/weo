import math
from discord.ext import commands
import aiohttp
import discord


class Currency(commands.Cog):
    """The description for Currency goes here."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["currency", "cc", "uc"])
    async def currency_convert(
        self,
        ctx: commands.Context,
        quantity: float,
        from_currency: str,
        to_currency: str,
    ):
        async with aiohttp.ClientSession(
            "https://cdn.jsdelivr.net",
        ) as session:
            async with session.get(
                f"/gh/fawazahmed0/currency-api@1/latest/currencies/{from_currency}/{to_currency}.json"
            ) as response:
                ratio = (await response.json()).get(to_currency)

                if ratio:
                    converted = quantity * float(ratio)

                    await ctx.reply(converted)
                else:
                    await ctx.reply("couldn't find cuwwency :3")


async def setup(bot):
    await bot.add_cog(Currency(bot))
