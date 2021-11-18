from discord import Embed
from discord.ext.commands import Bot, Cog
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option

import newmlbstats
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
                                create_option(name="player_name",
                                              description="Player to search for",
                                              option_type=3,
                                              required=True),
                                create_option(name="season",
                                              description="Specify a season other than this year's (year delta like '-1' works too)",
                                              option_type=3,
                                              required=False)
    ])
    async def mlb_stats(self, ctx: SlashContext, player_name: str, season=None):
        res = "```%s```" % newmlbstats.get_player_season_stats(player_name, year=season)
        await ctx.send(res)


def setup(bot: Bot):
    bot.add_cog(Baseball(bot))
