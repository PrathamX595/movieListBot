import discord
from discord.ext import commands
import dotenv
import os
dotenv.load_dotenv()

intent = discord.Intents.default()
intent.message_content = True
bot = commands.Bot(command_prefix='/', intents=intent)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

bot.run(os.getenv('TOKEN'))