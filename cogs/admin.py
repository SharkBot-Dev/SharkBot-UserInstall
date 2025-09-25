from discord import Client, Intents, Interaction, app_commands
from discord.ext import commands

class AdminCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    admin = app_commands.Group(name="admin", description="管理者専用コマンドです")

    @admin.command(name="reload", description="Cogをreloadします。")
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def reload(self, interaction: Interaction, cog名: str):
        await interaction.response.defer(ephemeral=True)
        if interaction.user.id != 1335428061541437531:
            return await interaction.followup.send(ephemeral=True, content="権限がありません。")
        await self.bot.reload_extension(f"cogs.{cog名}")
        await interaction.followup.send(ephemeral=True, content="リロードしました。")

    @admin.command(name="load", description="Cogをloadします。")
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def load_cog(self, interaction: Interaction, cog名: str):
        await interaction.response.defer(ephemeral=True)
        if interaction.user.id != 1335428061541437531:
            return await interaction.followup.send(ephemeral=True, content="権限がありません。")
        await self.bot.load_extension(f"cogs.{cog名}")
        await interaction.followup.send(ephemeral=True, content="ロードしました。")

    @admin.command(name="sync", description="スラッシュコマンドを同期します。")
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def sync(self, interaction: Interaction):
        await interaction.response.defer(ephemeral=True)
        if interaction.user.id != 1335428061541437531:
            return await interaction.followup.send(ephemeral=True, content="権限がありません。")
        await self.bot.tree.sync()
        await interaction.followup.send(ephemeral=True, content="スラッシュコマンドを同期しました。")

    @admin.command(name="echo", description="発言をします。")
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def echo(self, interaction: Interaction, 発言: str):
        await interaction.response.send_message(ephemeral=True, content="送信中・・")
        if interaction.user.id != 1335428061541437531:
            return await interaction.followup.send(ephemeral=True, content="権限がありません。")
        await interaction.followup.send(content=発言)
        await interaction.delete_original_response()

async def setup(bot: commands.Bot):
    await bot.add_cog(AdminCog(bot))