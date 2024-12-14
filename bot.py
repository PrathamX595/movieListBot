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
        try:
            global col
            col = db.create_collection(ctx.guild.name)
            await ctx.send("List created")
        except Exception as e:
            await ctx.send(f"An error occurred: {e}")

@bot.command()
async def list(ctx, gen):
    collections = db.list_collection_names()
    if ctx.guild.name in collections:
        col = db.get_collection(ctx.guild.name)
        if gen:
            pipeline = [
                {"$match": {"genre": gen}}
            ]
            data = col.aggregate(pipeline)
            if data:
                ctx.send(data)       #TODO:parse in a readable format
            else:
                ctx.send("no movies found")
        else:
            data = col.find()
            if data:
                ctx.send(data)       #TODO:parse in a readable format
            else:
                ctx.send("no movies found")
    else:
        ctx.send("404: No list found for this server, create a list by [/init] ")

bot.run(os.getenv('TOKEN'))