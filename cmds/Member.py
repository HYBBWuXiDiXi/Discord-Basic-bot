import datetime
import discord
import json
from discord.app_commands import Choice
from discord.ext import commands
from discord import app_commands
from Basic_bot.Core.init_cog import InitCog
from discord.utils import get


class Member(InitCog):

    # give someone a role by commands,example: ?add-role @user [true/false] [old-role's name] [new-role's name]
    # this example means user joined test and removed from test1 : ?add-role @user true test1 test
    # old-role can be multiple
    # true:remove from old-role and join new-role,false:join new-role directly
    @commands.command(name='add-role', help='给予身份组')
    @commands.is_owner()
    async def addrole(self, ctx, arg: discord.Member, arg1: bool, arg2: str, *, arg3: str):
        oldrole = get(ctx.guild.roles, name=arg2)
        newrole = get(ctx.guild.roles, name=arg3)
        await ctx.channel.purge(limit=1)
        if arg1:  # remove from old-role and join new-role
            await arg.remove_roles(oldrole)
            await arg.add_roles(newrole)
            await ctx.send(embed=discord.Embed(description=f'{arg} 已从 {oldrole} 移除，并加入到 {newrole}',
                                               colour=discord.Color.from_rgb(130, 156, 242)))
        else:  # dont remove other
            await arg.add_roles(newrole)
            await ctx.send(embed=discord.Embed(description=f'{arg} 已加入到 {newrole}',
                                               colour=discord.Color.from_rgb(130, 156, 242)))

    # kick member by command,example: ?kick @user
    @commands.command(name='kick', help='踢除用户')
    @commands.has_permissions(kick_members=True)
    async def kickmember(self, ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.channel.purge(limit=1)
        await ctx.send(embed=discord.Embed(description=f'{member} 已被踢出，原因:{reason}',
                                           colour=discord.Color.from_rgb(130, 156, 242)))

    # ban member by command,example: ?ban @user
    @commands.command(name='ban', help='封禁用户')
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.channel.purge(limit=1)
        await ctx.send(embed=discord.Embed(description=f'{member} 已被封禁，原因:{reason}',
                                           colour=discord.Color.from_rgb(130, 156, 242)))

    @app_commands.command(name='mute', description='静音用户')
    @app_commands.describe(reason='静音的原因')
    async def mute(self, interaction: discord.Interaction, member: discord.Member, *, reason: str = None):
        if interaction.user.guild_permissions.mute_members:
            try:
                voice_state = member.voice
                if voice_state:
                    await interaction.response.defer()
                    await member.edit(mute=True, reason=reason)
                    await interaction.followup.send(embed=discord.Embed(description=f'{member} 已被静音 , 原因 : {reason}',
                                                                        colour=discord.Color.from_rgb(130, 156, 242)))
                else:
                    await interaction.response.defer()
                    await interaction.followup.send(embed=discord.Embed(description=f'**{member}** 不在任何语音频道中',
                                                                        colour=discord.Color.from_rgb(130, 156, 242)))
            except Exception as e:
                print(e)
        else:
            await interaction.response.defer()
            await interaction.followup.send(embed=discord.Embed(description=f'{interaction.user.mention} 没有执行这项操作的权限',
                                                                colour=discord.Color.from_rgb(130, 156, 242)))

    @app_commands.command(name='timeout', description='禁言用户')
    @app_commands.rename(option='禁言时间')
    @app_commands.describe(reason='禁言的原因')
    @app_commands.choices(option=[
        Choice(name='60秒', value=0),
        Choice(name='5分钟', value=1),
        Choice(name='10分钟', value=2),
        Choice(name='1小时', value=3),
        Choice(name='1天', value=4),
        Choice(name='1周', value=5)
    ])
    async def timeout(self, interaction: discord.Interaction, member: discord.Member, option: int, *, reason: str = None):
        if interaction.user.guild_permissions.moderate_members:
            try:
                if option == 0:
                    await interaction.response.defer()
                    await member.timeout(datetime.timedelta(minutes=1.0), reason=reason)
                    await interaction.followup.send(
                        embed=discord.Embed(description=f'{member} 已被禁言 **1 分钟**, 原因 : {reason}',
                                            colour=discord.Color.from_rgb(130, 156, 242)))
                elif option == 1:
                    await interaction.response.defer()
                    await member.timeout(datetime.timedelta(minutes=5.0), reason=reason)
                    await interaction.followup.send(
                        embed=discord.Embed(description=f'{member} 已被禁言 **5 分钟**, 原因 : {reason}',
                                            colour=discord.Color.from_rgb(130, 156, 242)))
                elif option == 2:
                    await interaction.response.defer()
                    await member.timeout(datetime.timedelta(minutes=10.0), reason=reason)
                    await interaction.followup.send(
                        embed=discord.Embed(description=f'{member} 已被禁言 **10 分钟**, 原因 : {reason}',
                                            colour=discord.Color.from_rgb(130, 156, 242)))
                elif option == 3:
                    await interaction.response.defer()
                    await member.timeout(datetime.timedelta(hours=1.0), reason=reason)
                    await interaction.followup.send(
                        embed=discord.Embed(description=f'{member} 已被禁言 **1 小时**, 原因 : {reason}',
                                            colour=discord.Color.from_rgb(130, 156, 242)))
                elif option == 4:
                    await interaction.response.defer()
                    await member.timeout(datetime.timedelta(weeks=1.0), reason=reason)
                    await interaction.followup.send(
                        embed=discord.Embed(description=f'{member} 已被禁言 **1 天**, 原因 : {reason}',
                                            colour=discord.Color.from_rgb(130, 156, 242)))
                elif option == 5:
                    await interaction.response.defer()
                    await member.timeout(datetime.timedelta(minutes=1.0), reason=reason)
                    await interaction.followup.send(
                        embed=discord.Embed(description=f'{member} 已被禁言 **1 周**, 原因 : {reason}',
                                            colour=discord.Color.from_rgb(130, 156, 242)))
            except Exception as e:
                print(e)
        else:
            await interaction.response.defer()
            await interaction.followup.send(embed=discord.Embed(description=f'{interaction.user.mention} 没有执行这项操作的权限',
                                                                colour=discord.Color.from_rgb(130, 156, 242)))

    # unban member by command,example: ?unban @user
    @commands.command(name='unban', help='解封用户')
    @commands.has_permissions(ban_members=True)
    @commands.guild_only()
    async def unban(self, ctx, userId):
        user = discord.Object(id=userId)
        await ctx.guild.unban(user)
        await ctx.channel.purge(limit=1)
        await ctx.send(embed=discord.Embed(description=f'已解除 {userId} 的封禁',
                                           colour=discord.Color.from_rgb(130, 156, 242)))


async def setup(client):
    await client.add_cog(Member(client))
