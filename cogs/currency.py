from discord.ext import commands
import aiohttp


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
        to_currency = to_currency.lower()
        from_currency = from_currency.lower()
        async with aiohttp.ClientSession(
            "https://cdn.jsdelivr.net",
        ) as session:
            async with session.get(
                f"/npm/@fawazahmed0/currency-api@latest/v1/currencies/{from_currency}.min.json"
            ) as response:
                ratio = (await response.json()).get(from_currency, {}).get(to_currency)

                if ratio:
                    converted = quantity * float(ratio)

                    await ctx.reply(f"{converted:.2f}")
                else:
                    await ctx.reply("couldn't find cuwwency :3")


async def setup(bot):
    await bot.add_cog(Currency(bot))
