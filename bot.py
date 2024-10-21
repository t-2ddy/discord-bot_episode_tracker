import os
import time
import discord
from dotenv import load_dotenv
import asyncio
from discord.ext import commands
from discord import app_commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
user_id = os.getenv('USER_ID')

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

async def send_reminder(user_id):
    user = await bot.fetch_user(user_id)  # fetch user id to put into 'user' object
    await user.create_dm()
    await user.dm_channel.send(f'{user.name} ... ONE PIECE ... NOW !!!!')

@bot.event
async def on_ready():
    print(f'{bot.user.name} is ready')
    # send one at run
    await send_reminder(user_id)
    synced = await bot.tree.sync()
    print(f"Synced {len(synced)} command(s)")
    # send at time
    async def job():
        await send_reminder(user_id)
        
    # time the message
    while True:
        now = time.strftime("%H:%M") #get curr time
        if now == "20:30": #830 pm
            await job()
        await asyncio.sleep(60)

@bot.tree.command(name="test")
async def test(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hey {interaction.user.mention} this is a test for slash commands", ephemeral=True)


@bot.tree.command(name="epbookmark")
@app_commands.describe(episode_bookmark = "enter current episode number")
async def epbookmark(interaction: discord.Interaction, episode_bookmark: int):
    with open('ep.txt', 'w') as file:
        file.write(str(episode_bookmark))
    await interaction.response.send_message(f"You are now on episode {episode_bookmark}", ephemeral=True)


bot.tree.command(name="ep_number_check")
async def ep_number_check(interaction: discord.Interaction):
    with open('ep.txt', 'w') as file:
        current_ep = file.readlines()
    await interaction.response.send_message(f"Hey {interaction.user.mention} you are on episode {current_ep}")

bot.run(TOKEN)