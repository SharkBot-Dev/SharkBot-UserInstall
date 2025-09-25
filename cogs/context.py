from discord import Client, Intents, Interaction, app_commands
import discord
from discord.ext import commands
import aiohttp
from PIL import Image, ImageSequence, ImageEnhance, ImageDraw, ImageFont, ImageOps
import io

class ContextCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

async def fetch_avatar(user: discord.User):
    if user.avatar:
        url_a = f"https://cdn.discordapp.com/avatars/{user.id}/{user.avatar.key}"
    else:
        url_a = user.default_avatar.url
    async with aiohttp.ClientSession() as session:
        async with session.get(url_a, timeout=10) as resp:
            return await resp.read()

def wrap_text_with_ellipsis(text, font, draw, max_width, max_height, line_height):
    lines = []
    for raw_line in text.split("\n"):
        current_line = ""
        for char in raw_line:
            test_line = current_line + char
            bbox = draw.textbbox((0, 0), test_line, font=font)
            w = bbox[2] - bbox[0]
            if w <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = char

            if len(lines) * line_height >= max_height - line_height * 2:
                ellipsis = "…"
                while True:
                    bbox = draw.textbbox((0, 0), current_line + ellipsis, font=font)
                    if bbox[2] - bbox[0] <= max_width:
                        break
                    if len(current_line) == 0:
                        break
                    current_line = current_line[:-1]
                lines.append(current_line + ellipsis)
                return lines

        if current_line:
            lines.append(current_line)

    return lines

def create_quote_image(author, text, avatar_bytes, background, textcolor, color: bool):
        width, height = 800, 400
        background_color = background
        text_color = textcolor

        img = Image.new('RGB', (width, height), background_color)
        draw = ImageDraw.Draw(img)

        avatar_size = (400, 400)
        avatar = Image.open(io.BytesIO(avatar_bytes)).convert("RGBA")
        avatar = avatar.resize(avatar_size)

        mask = Image.new("L", avatar_size, 255)
        for x in range(avatar_size[0]):
            alpha = 255 if x < avatar_size[0] // 2 else int(255 * (1 - (x - avatar_size[0] // 2) / (avatar_size[0] / 2)))
            for y in range(avatar_size[1]):
                mask.putpixel((x, y), alpha)
        avatar.putalpha(mask)

        img.paste(avatar, (0, height - avatar_size[1]), avatar)

        try:
            font = ImageFont.truetype("data/DiscordFont.ttf", 30)
            name_font = ImageFont.truetype("data/DiscordFont.ttf", 20)
        except:
            font = ImageFont.load_default()
            name_font = ImageFont.load_default()

        text_x = 420
        max_text_width = width - text_x - 50

        max_text_height = height - 80
        line_height = font.size + 10

        lines = wrap_text_with_ellipsis(text, font, draw, max_text_width, max_text_height, line_height)

        total_lines = len(lines)
        line_height = font.size + 10
        text_block_height = total_lines * line_height
        text_y = (height - text_block_height) // 2

        for i, line in enumerate(lines):
            bbox = draw.textbbox((0, 0), line, font=font)
            line_width = bbox[2] - bbox[0]
            draw.text(
                ((width + text_x - 50 - line_width) // 2, text_y + i * line_height),
                line,
                fill=text_color,
                font=font
            )

        author_text = f"- {author}"
        bbox = draw.textbbox((0, 0), author_text, font=name_font)
        author_width = bbox[2] - bbox[0]
        author_x = (width + text_x - 50 - author_width) // 2
        author_y = text_y + len(lines) * line_height + 10

        draw.text((author_x, author_y), author_text, font=name_font, fill=text_color)

        if color:

            return img
        else:
            return img.convert("L")

@app_commands.context_menu(name="Make it a Quote")
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def miq_command(interaction: discord.Interaction, message: discord.Message):
    if not message.content:
        return await interaction.response.send_message("メッセージがありません。", ephemeral=True)
    await interaction.response.send_message(ephemeral=True, content="作成しています・・")
    try:
        avatar = message.author
        av = await fetch_avatar(avatar)
        miq = create_quote_image(
            message.author.display_name,
            message.content,
            av,
            (0, 0, 0),
            (255, 255, 255),
            True
        )
        with io.BytesIO() as image_binary:
            miq.save(image_binary, 'PNG')
            image_binary.seek(0)
            await interaction.followup.send(file=discord.File(fp=image_binary, filename='quote.png'))
            await interaction.followup.send("作成完了！", ephemeral=True)
    except aiohttp.ClientOSError as e:
        await interaction.followup.send("ClientOSエラーが発生しました。\n再度コマンドを実行してみてください。", ephemeral=True)
        return
    except:
        return await interaction.user.send(f"エラーが発生しました。")
    
async def setup(bot: commands.Bot):
    await bot.add_cog(ContextCog(bot))
    bot.tree.add_command(miq_command)