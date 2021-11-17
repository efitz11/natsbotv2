from discord import Embed
from discord.ext.commands import Bot, Cog
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option

import utils


class Baseball(Cog):
    dev_ids = utils.get_dev_guild_ids()
    def __init__(self, bot: Bot):
        self.bot = bot

    @cog_ext.cog_slash(name="test", guild_ids=dev_ids)
    async def _test(self, ctx: SlashContext):
        embed = Embed(title="Embed Test")
        await ctx.send(embed=embed)

    # @cog_ext.cog_slash(name="mlb", guild_ids=dev_ids, description="display MLB info")
    # async def _mlb(self, ctx: SlashContext):
    #     await ctx.send("test output")

    @cog_ext.cog_subcommand(base="mlb", guild_ids=dev_ids, name="stats", description="display MLB player stats",
                            options=[
        create_option(name="season",
                      description="Specify a season other than this year's",
                      option_type=3,
                      required=False)
    ])
    async def mlb_stats(self, ctx: SlashContext, player_name: str, season:str):
        await ctx.send("mlb stats for %s!" % player_name)


def setup(bot: Bot):
    bot.add_cog(Baseball(bot))
