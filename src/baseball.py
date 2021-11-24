from datetime import date, datetime

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

    def get_delta(self, arg):
        delta = ""
        if len(arg) > 0 and (arg[-1].startswith('-') or arg[-1].startswith('+')):
            delta = arg
        elif len(arg) > 0 and len(arg.split('/')) in [2, 3]:
            if arg.split('/')[0].isdigit():
                delta = self.convert_date_to_delta(arg)
        elif len(arg) > 0 and arg.lower() in ['yesterday', 'tomorrow']:
            if arg == 'yesterday':
                delta = "-1"
            elif arg == 'tomorrow':
                delta = "+1"
        return delta

    def convert_date_to_delta(self, args):
        now = datetime.now().date()
        datelist = args.split('/')
        if len(datelist) == 2:
            datelist.append(str(now.year))
        if len(datelist[2]) == 2:
            if int("20" + datelist[2]) <= now.year:
                datelist[2] = "20" + datelist[2]
            else:
                datelist[2] = "19" + datelist[2]
        other = date(int(datelist[2]), int(datelist[0]), int(datelist[1]))
        delta = other - now
        direction = ''
        if delta.days > 0:
            direction = '+'
        return direction + str(delta.days)

    # @cog_ext.cog_slash(name="test", guild_ids=dev_ids)
    # async def _test(self, ctx: SlashContext):
    #     embed = Embed(title="Embed Test")
        # await ctx.send(embed=embed)

    # @cog_ext.cog_slash(name="mlb", guild_ids=dev_ids, description="display MLB info")
    # async def _mlb(self, ctx: SlashContext):
    #     await ctx.send("test output")

    @cog_ext.cog_slash(guild_ids=dev_ids, name="scores", description="display MLB scores",
                       options=[
                           create_option(name="filter",
                                         description="team filter (team name, league, division)",
                                         option_type=3,
                                         required=False),
                           create_option(name="t_delta",
                                         description="Specify day other than today. +/- days, mm/dd, mm/dd/yy, or 'yesterday'/'tomorrow' all work.",
                                         option_type=3,
                                         required=False)
                       ])
    async def scores(self, ctx: SlashContext, filter="", t_delta=None):
        filter = filter.lower()
        if t_delta is not None:
            t_delta = self.get_delta(t_delta)
        output, numgames = newmlbstats.print_games(filter, delta=t_delta)
        if len(output) > 0:
            await ctx.send("```python\n" + output + "```")
        else:
            await ctx.send("no games found")

    @cog_ext.cog_slash(guild_ids=dev_ids, name="stats", description="display MLB player stats",
                            options=[
                                create_option(name="player_name",
                                              description="Player to search for",
                                              option_type=3,
                                              required=True),
                                create_option(name="season",
                                              description="Specify a season other than this year's (year delta like '-1' works too)",
                                              option_type=3,
                                              required=False),
                                create_option(name="force_pitching",
                                              description="Force pitching stats instead of batting",
                                              option_type=5,
                                              required=False),
                                create_option(name="force_batting",
                                              description="Force batting stats instead of pitching",
                                              option_type=5,
                                              required=False),
                            ])
    async def mlb_stats(self, ctx: SlashContext, player_name: str, season=None, force_pitching=False, force_batting=False):
        type = None
        if force_pitching:
            type = "pitching"
        elif force_batting:
            type = "hitting"
        res = "```%s```" % newmlbstats.get_player_season_stats(player_name, year=season, type=type)
        await ctx.send(res)


def setup(bot: Bot):
    bot.add_cog(Baseball(bot))
