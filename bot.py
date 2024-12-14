import discord
from discord.ext import commands
import dotenv
import os
import pymongo
dotenv.load_dotenv()

mongoClient = pymongo.MongoClient(os.getenv('MONGO'))
db = mongoClient["MovieBotDb"]

intent = discord.Intents.default()
intent.message_content = True
bot = commands.Bot(command_prefix='/', intents=intent)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command()
async def init(ctx):
    collections = db.list_collection_names()
    if ctx.guild.name in collections:
        await ctx.send("list already exists")
    else:
        global col 
        col = db.create_collection(ctx.guild.name)
        await ctx.send("List created")

@bot.command()
async def list(ctx):
    collections = db.list_collection_names()
    if ctx.guild.name in collections:
        data = col.find()
        if data:
            ctx.send(data)       #TODO:parse in a readable format
        else:
            ctx.send("no movies found")

bot.run(os.getenv('TOKEN'))