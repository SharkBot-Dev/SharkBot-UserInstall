from discord import Client, Intents, Interaction, app_commands
import discord
from discord.ext import commands
import datetime

PERMISSION_TRANSLATIONS = {
    "administrator": "管理者",
    "view_audit_log": "監査ログの表示",
    "view_guild_insights": "サーバーインサイトの表示",
    "manage_guild": "サーバーの管理",
    "manage_roles": "ロールの管理",
    "manage_channels": "チャンネルの管理",
    "kick_members": "メンバーのキック",
    "ban_members": "メンバーのBAN",
    "create_instant_invite": "招待の作成",
    "change_nickname": "ニックネームの変更",
    "manage_nicknames": "ニックネームの管理",
    "manage_emojis_and_stickers": "絵文字とステッカーの管理",
    "manage_webhooks": "Webhookの管理",
    "view_channel": "チャンネルの閲覧",
    "send_messages": "メッセージの送信",
    "send_tts_messages": "TTSメッセージの送信",
    "manage_messages": "メッセージの管理",
    "embed_links": "埋め込みリンクの送信",
    "attach_files": "ファイルの添付",
    "read_message_history": "メッセージ履歴の閲覧",
    "read_messages": "メッセージの閲覧",
    "external_emojis": "絵文字を管理",
    "mention_everyone": "everyone のメンション",
    "use_external_emojis": "外部絵文字の使用",
    "use_external_stickers": "外部ステッカーの使用",
    "add_reactions": "リアクションの追加",
    "connect": "ボイスチャンネルへの接続",
    "speak": "発言",
    "stream": "配信",
    "mute_members": "メンバーのミュート",
    "deafen_members": "メンバーのスピーカーミュート",
    "move_members": "ボイスチャンネルの移動",
    "use_vad": "音声検出の使用",
    "priority_speaker": "優先スピーカー",
    "request_to_speak": "発言リクエスト",
    "manage_events": "イベントの管理",
    "use_application_commands": "アプリケーションコマンドの使用",
    "manage_threads": "スレッドの管理",
    "create_public_threads": "公開スレッドの作成",
    "create_private_threads": "非公開スレッドの作成",
    "send_messages_in_threads": "スレッド内でのメッセージ送信",
    "use_embedded_activities": "アクティビティの使用",
    "moderate_members": "メンバーのタイムアウト",
    "use_soundboard": "サウンドボードの使用",
    "manage_expressions": "絵文字などの管理",
    "create_events": "イベントの作成",
    "create_expressions": "絵文字などの作成",
    "use_external_sounds": "外部のサウンドボードなどの使用",
    "use_external_apps": "外部アプリケーションの使用",
    "view_creator_monetization_analytics": "ロールサブスクリプションの分析情報を表示",
    "send_voice_messages": "ボイスメッセージの送信",
    "send_polls": "投票の作成",
    "external_stickers": "外部のスタンプの使用",
    "use_voice_activation": "ボイスチャンネルでの音声検出の使用",
}

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
        missing_perms = [
            PERMISSION_TRANSLATIONS.get(perm, perm)
            for perm in interaction.app_permissions
        ]

        await interaction.response.defer()
        embed = discord.Embed(title="チャンネルの情報")
        embed.add_field(name="チャンネル名", value=interaction.channel.name, inline=False)
        embed.add_field(name="チャンネルID", value=str(interaction.channel_id), inline=False)
        embed.add_field(name="Botのチャンネル権限", value=f"{', '.join(missing_perms)}", inline=False)
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