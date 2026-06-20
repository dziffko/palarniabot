import os
import sqlite3
import discord
from discord.ext import commands

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Database
conn = sqlite3.connect("cigs.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS cigarettes (
    user_id TEXT PRIMARY KEY,
    count INTEGER NOT NULL
)
""")
conn.commit()


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


@bot.command()
async def smoke(ctx):
    user_id = str(ctx.author.id)

    cursor.execute(
        "SELECT count FROM cigarettes WHERE user_id = ?",
        (user_id,)
    )
    result = cursor.fetchone()

    if result is None:
        count = 1
        cursor.execute(
            "INSERT INTO cigarettes (user_id, count) VALUES (?, ?)",
            (user_id, count)
        )
    else:
        count = result[0] + 1
        cursor.execute(
            "UPDATE cigarettes SET count = ? WHERE user_id = ?",
            (count, user_id)
        )

    conn.commit()

    await ctx.send(
        "🚬 You light up a cigarette. Smoke comes out of your mouth. What a delightful sensation!"
    )


@bot.command()
async def cigs(ctx):
    user_id = str(ctx.author.id)

    cursor.execute(
        "SELECT count FROM cigarettes WHERE user_id = ?",
        (user_id,)
    )
    result = cursor.fetchone()

    count = result[0] if result else 0

    await ctx.send(
        f"🚬 {ctx.author.mention}, you have smoked {count} cigarettes."
    )


@bot.command()
async def topcigs(ctx):
    cursor.execute("""
        SELECT user_id, count
        FROM cigarettes
        ORDER BY count DESC
        LIMIT 10
    """)

    results = cursor.fetchall()

    if not results:
        await ctx.send("🚬 Nobody has smoked a cigarette yet.")
        return

    msg = "🏆 **Cigarette Leaderboard**\n\n"

    for i, (user_id, count) in enumerate(results, start=1):
        try:
            user = await bot.fetch_user(int(user_id))
            username = user.name
        except:
            username = f"User {user_id}"

        msg += f"**{i}.** {username} — {count} 🚬\n"

    await ctx.send(msg)


bot.run(TOKEN)
