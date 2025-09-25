from discord import Client, Intents, Interaction, app_commands
import discord
from discord.ext import commands

class ToolsCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    tools = app_commands.Group(name="tools", description="ツール関連のコマンドです。")

    @tools.command(name="afk", description="AFKを設定します。")
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def afk(self, interaction: Interaction, 理由: str, 終わったらやること: str = "まだ予定がありません。"):
        await interaction.response.defer()
        database = self.bot.async_db["Main"].AFK
        await database.replace_one(
            {"User": interaction.user.id}, 
            {"User": interaction.user.id, "Reason": 理由, "End": 終わったらやること}, 
            upsert=True
        )
        await interaction.followup.send(embed=discord.Embed(title="AFKを設定しました。", description=f"{理由}", color=discord.Color.green()))

    @tools.command(name="invite-bot", description="Botの招待リンクを生成します。")
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def invite_bot(self, interaction: Interaction, botのid: discord.User):
        if not botのid.bot:
            return await interaction.response.send_message(content="BotのIDを指定してください。", ephemeral=True)
        await interaction.response.defer()
        embed=discord.Embed(title=f"{botのid}を招待する。", description=f"""# [☢️管理者権限で招待](https://discord.com/oauth2/authorize?client_id={botのid.id}&permissions=8&integration_type=0&scope=bot+applications.commands)
# [🖊️権限を選んで招待](https://discord.com/oauth2/authorize?client_id={botのid.id}&permissions=1759218604441591&integration_type=0&scope=bot+applications.commands)
# [😆権限なしで招待](https://discord.com/oauth2/authorize?client_id={botのid.id}&permissions=0&integration_type=0&scope=bot+applications.commands)""", color=discord.Color.green())
        await interaction.followup.send(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(ToolsCog(bot))