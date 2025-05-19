from discord.ext import commands
import aiohttp

from discord import app_commands
import discord


async def convert(quantity: float, from_currency: str, to_currency: str) -> float:
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

                return converted
            else:
                raise Exception("couldnt find cuwwency 3:")


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
        converted_value = await convert(
            quantity=quantity, from_currency=from_currency, to_currency=to_currency
        )

        await ctx.reply(f"{converted_value:.2f}")

    @app_commands.command(name="currency_convert")
    @app_commands.describe(
        quantity="Amount of the currency to be converted",
        from_currency="Origin currency",
        to_currency="Target currency",
    )
    async def app_currency_convert(
        self,
        interaction: discord.Interaction,
        quantity: float,
        from_currency: str,
        to_currency: str,
    ):
        converted_value = await convert(
            quantity=quantity, from_currency=from_currency, to_currency=to_currency
        )

        await interaction.response.send_message(
            f"{quantity:.2f} {from_currency.upper()} -> {converted_value:.2f} {to_currency.upper()}"
        )


async def setup(bot):
    await bot.add_cog(Currency(bot))
