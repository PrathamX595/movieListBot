# Movie Listing Bot

This is a Discord bot designed to help you and your friends manage movies. With this bot, you can create a list of movies, add new movies, list all movies.

## Features

- **Initialize Movie List**: Create a movie list for your server.
- **Add Movies**: Add movies to your server's list with optional genre specification.
- **List Movies**: List all movies or filter movies by genre.
- **Remove Movies**: Remove movies from your server's list.

## Commands

- `/init`: Initialize a movie list for your server.
- `/add <movie_name> [genre]`: Add a movie to your server's list.
- `/list_movies [genre]`: List all movies or filter by genre.
- `/remove <movie_name>`: Remove a movie from your server's list.

## Setup

1. Clone the repository.
2. Install the required dependencies using `pip install -r requirements.txt`.
3. Create a `.env` file based on the `.env.example` file and fill in your Discord bot token and MongoDB connection string.
4. Run the bot using `python bot.py`.

## Requirements

- Python 3.8+
- MongoDB
- Discord Bot Token

## Installation

```bash
git clone https://github.com/PrathamX595/movieListBot.git
cd movieListBot
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the root directory of the project and add your configuration:

```bash
TOKEN='YOUR DISCORD BOT TOKEN'
MONGO='YOUR MongoDB string'
```

## Running the Bot

```bash
python bot.py
```

Enjoy managing your movies with your friends!

