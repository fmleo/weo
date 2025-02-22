from discord.ext import commands
import discord
from random import shuffle

class RNG(commands.Cog):
    """The description for RNG goes here."""

    @commands.command(aliases=["roll"])
    async def roletar(self, ctx: commands.Context, n_groups: int = 2):
        """Distribui os membros de uma chamada de voz aleatoriamente em grupos."""
        voice_channel = ctx.author.voice.channel
        if voice_channel is None:
            await ctx.reply("Você precisa estar em um canal de voz para usar este comando.")
            return

        members = voice_channel.members
        if len(members) < n_groups:
            await ctx.reply("Não há membros suficientes para dividir em tantos grupos.")
            return

        members = [member.display_name for member in members if not member.bot]
        members = sorted(members)
        shuffle(members)
        groups = [[] for _ in range(n_groups)]

        for i, member in enumerate(members):
            groups[i % n_groups].append(member)

        embed = discord.Embed(title="Grupos", color=discord.Color.green())
        for i, group in enumerate(groups):
            embed.add_field(name=f"Grupo {i + 1}", value="\n".join(group), inline=False)

        await ctx.reply(embed=embed)

    def __init__(self, bot):
        self.bot = bot

async def setup(bot):
    await bot.add_cog(RNG(bot))
