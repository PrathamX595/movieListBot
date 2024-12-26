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
        await ctx.send("List already exists")
    else:
        try:
            col = db.create_collection(ctx.guild.name)
            await ctx.send("List created")
        except Exception as e:
            await ctx.send(f"An error occurred: {e}")

@bot.command()
async def list_movies(ctx, gen: str = None):
    collections = db.list_collection_names()
    if ctx.guild.name in collections:
        col = db.get_collection(ctx.guild.name)
        if gen:
            pipeline = [{"$match": {"genre": gen}}]
            data = list(col.aggregate(pipeline))
            if data:
                movies = "\n".join([movie['name'] for movie in data])
                await ctx.send(f"**Movies in genre '{gen}':**\n{movies}")
            else:
                await ctx.send(f"No movies found in genre '{gen}'.")
        else:
            data = list(col.find())
            if data:
                movies = "\n".join([movie['name'] for movie in data])
                await ctx.send(f"**All Movies:**\n{movies}")
            else:
                await ctx.send("No movies found.")
    else:
        await ctx.send("404: No list found for this server, create a list by [/init].")

@bot.command()
async def add(ctx, movie_name: str, genre: str = None):
    collections = db.list_collection_names()
    if ctx.guild.name in collections:
        col = db.get_collection(ctx.guild.name)
        movie = {"name": movie_name, "genre": genre}
        try:
            res = col.insert_one(movie)
            await ctx.send(f"Movie '{movie_name}' added successfully!")
        except Exception as e:
            await ctx.send(f"An error occurred: {e}")
    else:
        await ctx.send("404: No list found for this server, create a list by [/init].")

@bot.command()
async def remove(ctx, movie_name: str):
    collections = db.list_collection_names()
    if ctx.guild.name in collections:
        col = db.get_collection(ctx.guild.name)
        try:
            res = col.find_one_and_delete({"name": movie_name})
            if res:
                await ctx.send(f"Movie '{movie_name}' deleted successfully!")
            else:
                await ctx.send(f"Movie '{movie_name}' not found.")
        except Exception as e:
            await ctx.send(f"An error occurred: {e}")
    else:
        await ctx.send("404: No list found for this server, create a list by [/init].")

bot.run(os.getenv('TOKEN'))