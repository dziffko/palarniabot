import discord
from discord.ext import commands
import json
import os

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

DATA_FILE = "cigs.json"


def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)


@bot.event
async def on_ready():
    print(f"Zalogowano jako {bot.user}")


@bot.command()
async def smoke(ctx):
    data = load_data()
    user = str(ctx.author.id)

    data[user] = data.get(user, 0) + 1
    save_data(data)

    await ctx.send("🚬 You light up a cigarette. Smoke comes out of your mouth. What a delightful sensation!")


@bot.command()
async def cigs(ctx):
    data = load_data()
    user = str(ctx.author.id)

    await ctx.send(f"🚬 You smoked {data.get(user, 0)} cigarettes")


bot.run(TOKEN)
