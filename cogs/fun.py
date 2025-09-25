from discord import Client, Intents, Interaction, app_commands
import discord
from discord.ext import commands
import re
import io
import aiohttp
import random
import asyncio
from PIL import Image, ImageDraw, ImageFont, ImageOps
import json

class FunCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    fun = app_commands.Group(name="fun", description="面白いコマンドです。")

    @fun.command(name="roll", description="さいころをふります。")
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def roll(self, interaction: Interaction,  何面か: str):
        match = re.fullmatch(r'(\d+)d(\d+)', 何面か)
        if not match:
            return await interaction.response.send_message(content="形式が正しくありません。\n例: `5d3`", ephemeral=True)
        num_dice, sides = map(int, match.groups())
        if num_dice > 100:
            return await interaction.response.send_message(content="サイコロの個数は 100 以下にしてください", ephemeral=True)
        if sides > 100:
            return await interaction.response.send_message("100 面以上のサイコロは使えません。", ephemeral=True)
        rolls = [random.randint(1, sides) for _ in range(num_dice)]
        str_rolls = [str(r) for r in rolls]
        await interaction.response.send_message(f"🎲 {interaction.user.mention}: {', '.join(str_rolls)} → {sum(rolls)}")

    image = app_commands.Group(name="image", description="画像関連のコマンドです。")

    @image.command(name="5000", description="5000兆円ほしい！")
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def _5000(self, interaction: Interaction, 上: str, 下: str, noアルファ: bool = None):
        if noアルファ:
            if noアルファ == False:
                msg = await interaction.response.send_message(embed=discord.Embed(title="5000兆円ほしい！", color=discord.Color.green()).set_image(url=f"https://gsapi.cbrx.io/image?top={上}&bottom={下}"))
            else:
                msg = await interaction.response.send_message(embed=discord.Embed(title="5000兆円ほしい！", color=discord.Color.green()).set_image(url=f"https://gsapi.cbrx.io/image?top={上}&bottom={下}&noalpha=true"))
        else:
            msg = await interaction.response.send_message(embed=discord.Embed(title="5000兆円ほしい！", color=discord.Color.green()).set_image(url=f"https://gsapi.cbrx.io/image?top={上}&bottom={下}"))

    @image.command(name="cat", description="ネコの画像を生成します。")
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def _cat(self, interaction: Interaction):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://api.thecatapi.com/v1/images/search?size=med&mime_types=jpg&format=json&has_breeds=true&order=RANDOM&page=0&limit=1"
            ) as cat:
                msg = await interaction.response.send_message(
                    embed=discord.Embed(
                        title="猫の画像", color=discord.Color.green()
                    ).set_image(url=json.loads(await cat.text())[0]["url"])
                )

    @image.command(name="dog", description="犬の画像を生成します。")
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def _dog(self, interaction: discord.Interaction):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://dog.ceo/api/breeds/image/random") as dog_:
                await interaction.response.send_message(
                    embed=discord.Embed(
                        title="犬の画像", color=discord.Color.green()
                    ).set_image(url=f"{json.loads(await dog_.text())['message']}")
                )

    @image.command(name="textmoji", description="テキストを絵文字にします。")
    @app_commands.choices(色=[
        app_commands.Choice(name='赤',value="FF0000"),
        app_commands.Choice(name='青',value="1111FF"),
        app_commands.Choice(name="黄", value="FFFF00"),
        app_commands.Choice(name='黒',value="000000"),
    ])
    async def textmoji(self, interaction: Interaction, 色: app_commands.Choice[str], テキスト: str, 正方形にするか: bool):
        await interaction.response.defer()
        def make_text(text: str, color: str, sq: bool):
            font = ImageFont.truetype("data/DiscordFont.ttf", 50)

            dummy_img = Image.new("RGBA", (1, 1))
            draw_dummy = ImageDraw.Draw(dummy_img)
            bbox = draw_dummy.textbbox((0, 0), text, font=font)
            text_w = bbox[2] - bbox[0]
            text_h = bbox[3] - bbox[1]

            padding = 0
            img = Image.new("RGBA", (text_w + padding*2, text_h + padding*2), (255, 255, 255, 0))
            draw = ImageDraw.Draw(img)

            draw.text((padding - bbox[0], padding - bbox[1]), text, fill=f"#{color}", font=font)

            if sq:
                img = img.resize((200, 200))

            i = io.BytesIO()
            img.save(i, format="PNG")
            i.seek(0)
            return i
                
        image = await asyncio.to_thread(make_text, テキスト, 色.value, 正方形にするか)

        await interaction.followup.send(
            file=discord.File(image, "emoji.png")
        )
        image.close()

async def setup(bot: commands.Bot):
    await bot.add_cog(FunCog(bot))