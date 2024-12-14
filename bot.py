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
async def list(ctx):
    collections = db.list_collection_names()
    if ctx.guild.name in collections:
        col = db.get_collection(ctx.guild.name)
        if ctx.message:
            pipeline = [
                {"$match": {"genre": ctx.message}}
            ]
            data = col.aggregate(pipeline)
            if data:
                await ctx.send(data)       #TODO:parse in a readable format
            else:
                await ctx.send("no movies found")
        else:
            data = col.find()
            if data:
                await ctx.send(data)       #TODO:parse in a readable format
            else:
                await ctx.send("no movies found")
    else:
       await ctx.send("404: No list found for this server, create a list by [/init] ")

@bot.command()
async def add(ctx):
    collections = db.list_collection_names()
    if ctx.guild.name in collections:
        col = db.get_collection(ctx.guild.name)
        if ctx.message:
            movie = {"name": ctx.message, "genere": ctx.message}
            try:
                res = col.insert_one(movie)
                await ctx.send("movie added!", res)
            except Exception as e:
                await ctx.send(f"An error occurred: {e}")
        else:
            await ctx.send("give a movie name with the proper genere")
    else:
        await ctx.send("404: No list found for this server, create a list by [/init] ")

@bot.command()
async def remove(ctx):
    collections = db.list_collection_names()
    if ctx.guild.name in collections:
        col = db.get_collection(ctx.guild.name)
        if ctx.message:
            try:
                res = col.find_one_and_delete(ctx.message)
                await ctx.send("movie deleted!", res)
            except Exception as e:
                await ctx.send(f"An error occurred: {e}")
        else:
            await ctx.send("give a movie name")
    else:
        await ctx.send("404: No list found for this server, create a list by [/init] ")

bot.run(os.getenv('TOKEN'))