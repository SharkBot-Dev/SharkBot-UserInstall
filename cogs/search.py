from discord import Client, Intents, Interaction, app_commands
import discord
from discord.ext import commands
import datetime

class SearchCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    search = app_commands.Group(name="search", description="検索関連のコマンドです。")

    @search.command(name="user", description="ユーザーを検索します。")
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def user(self, interaction: Interaction, ユーザー: discord.User):
        await interaction.response.defer()
        await interaction.followup.send(embed=discord.Embed(title=f"{ユーザー.display_name}の情報", color=discord.Color.green(), description=f"**名前**: {ユーザー.name}\n**ID**: {ユーザー.id}\n**アカウント作成日**: {ユーザー.created_at}\n**Bot?**: {"はい" if ユーザー.bot else "いいえ"}")
                                        .set_thumbnail(url=ユーザー.avatar.url if ユーザー.avatar else ユーザー.default_avatar.url))

    @search.command(name="avatar", description="アバターを検索します。")
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def avatar_(self, interaction: Interaction, ユーザー: discord.User):
        await interaction.response.defer()
        await interaction.followup.send(embed=discord.Embed(title=f"{ユーザー.display_name}のアバター", color=discord.Color.green()).set_image(url=ユーザー.avatar.url if ユーザー.avatar else ユーザー.default_avatar.url))

    @search.command(name="channel", description="コマンドを実行したチャンネルを検索します。")
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def channel_(self, interaction: Interaction):
        await interaction.response.defer()
        embed = discord.Embed(title="チャンネルの情報", color=discord.Color.green())
        embed.add_field(name="チャンネル名", value=interaction.channel.name, inline=False)
        embed.add_field(name="チャンネルID", value=str(interaction.channel_id), inline=False)
        embed.add_field(name="NSFWか", value="はい" if interaction.channel.nsfw else "いいえ", inline=False)
        await interaction.followup.send(embed=embed)
    
    @search.command(name="invite", description="招待リンクを検索します。")
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def invite(self, interaction: Interaction, 招待リンク: str):
        await interaction.response.defer()
        try:
            JST = datetime.timezone(datetime.timedelta(hours=9))
            invite = await self.bot.fetch_invite(招待リンク)
            if not invite:
                return await interaction.followup.send(embed=discord.Embed(title="招待リンクが見つかりません。", color=discord.Color.green()))
            embed = discord.Embed(title="招待リンクの情報", color=discord.Color.green()).add_field(name="サーバー名", value=f"{invite.guild.name}", inline=False).add_field(name="サーバーid", value=f"{invite.guild.id}", inline=False).add_field(name="招待リンク作成者", value=f"{invite.inviter.display_name if invite.inviter else "不明"} ({invite.inviter.id if invite.inviter else "不明"})", inline=False).add_field(name="招待リンクの使用回数", value=f"{invite.uses if invite.uses else "0"} / {invite.max_uses if invite.max_uses else "無限"}", inline=False)
            embed.add_field(name="チャンネル", value=f"{invite.channel.name if invite.channel else "不明"} ({invite.channel.id if invite.channel else "不明"})", inline=False)
            embed.add_field(name="メンバー数", value=f"{invite.approximate_member_count if invite.approximate_member_count else "不明"}", inline=False)
            embed.add_field(name="オンライン数", value=f"{invite.approximate_presence_count if invite.approximate_presence_count else "不明"}", inline=False)
            embed.add_field(name="作成時刻", value=f"{invite.created_at.astimezone(JST) if invite.created_at else "不明"}", inline=False)
            if invite.guild.icon:
                embed.set_thumbnail(url=invite.guild.icon.url)
            await interaction.followup.send(embed=embed)
        except:
            return await interaction.followup.send(embed=discord.Embed(title="招待リンクが見つかりません。", color=discord.Color.green()))

async def setup(bot: commands.Bot):
    await bot.add_cog(SearchCog(bot))