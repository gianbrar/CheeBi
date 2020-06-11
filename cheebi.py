import discord
import sys
import hashlib
import time
from discord.ext import commands
from discord.ext.commands import Bot

hashes = [
  "2a1e72f48ec4b77d821be3243f6b5757ab0bd6a76c8ee07fe1091203f9ee4b9b87f1ed6feca3f403466c1d54dcd6165810ed1a98aba41674d8d4bcc8440320fd",
  "9f5ff27bae96e312e021d2e84b3ea04b47c59cd3e610b2d0be06fd141b61eb25b5e1c1c9343b4fe93a63fde20117de4f534218ac05f24bc0d7f7d0c30020f484"
]

client = Bot(command_prefix=".")
client.remove_command("help")

if len(sys.argv) > 1:
  token = sys.argv[1]
else:
  token = open("token.txt", 'r')
  token = token.read()

@client.event
async def on_ready():
  print("CheeBi activated at " + time.asctime(time.localtime(time.time())))
  await client.change_presence(status=discord.Status.online, activity=discord.Game(name='To learn, type ".help"'))


@client.command()
async def help(ctx):
  await ctx.send("```\nHi there! I'm CheeBi. Here's some of what I can do:\n```")

@client.command()
async def shutdown(ctx):
  if hashlib.sha3_512(str(ctx.message.author.id).encode("utf-8")).hexdigest() in hashes:
    await ctx.send("Shutting down & shutting up...")
    await client.logout()
  else:
    await ctx.send("You are not authorized to use that command.")

client.run(token)