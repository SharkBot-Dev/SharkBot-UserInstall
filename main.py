from discord import Client, Intents, Interaction
from discord.ext import commands
import discord
import json
import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

class SharkBotUser(commands.AutoShardedBot):
    def __init__(self):
        super().__init__(
            command_prefix="u!",
            help_command=None,
            intents=discord.Intents.default(),
        )
        print("InitDone")
        self.async_db = AsyncIOMotorClient("mongodb://localhost:27017")

client = SharkBotUser()

@client.event
async def setup_hook():
    for cog in os.listdir("cogs"):
        if cog.endswith(".py"):
            await client.load_extension(f"cogs.{cog[:-3]}")
    await client.tree.sync()

client.run(os.environ.get('TOKEN'))