import discord
import sys
import time
from discord.ext import commands
from discord.ext.commands import Bot
token = open("token.txt", 'r')
token = token.read()

client = Bot(command_prefix=".")
client.remove_command("help")
if len(sys.argv) > 1:
  token = sys.argv[1]

@client.event
async def on_ready():
  print("CheeBi activated at " + time.asctime(time.localtime(time.time())))

client.run(token)