import asyncio
from discord.ext import commands
import discord

from discord.utils import escape_markdown, escape_mentions

from RestrictedPython import compile_restricted

from cogs.utils import restricted_globals


def get_code_output(code: str) -> str:
    try:
        bytecode = compile_restricted(code, filename="<string>", mode="exec")
        locals_dict = {}
        exec(bytecode, restricted_globals, locals_dict)
        # await ctx.reply(f"```py\n{code}```")
        return f"`{escape_mentions(escape_markdown(locals_dict.get('result')))}`"
    except Exception as e:
        return f"nuh uh: `{escape_mentions(escape_markdown(str(e)))}`"


class Eval(commands.Cog):
    """The description for Eval goes here."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def eval(self, ctx: commands.Context, *, code: str):
        code = code.strip("`")
        code = code.strip()
        code = code.replace("py", "", 1)

        if not code.startswith("print") and "\n" not in code:
            code = f"print({code})"

        code = f"{code}\nresult = printed"

        try:
            async with asyncio.timeout(5):
                response = await asyncio.to_thread(get_code_output, code)
                response = f"{response}"
        except TimeoutError:
            response = "command execution lasted more than 5 seconds please stop whatever youre trying :3"

        await ctx.reply(response)


async def setup(bot):
    await bot.add_cog(Eval(bot))
