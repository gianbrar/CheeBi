import discord
from discord.ext import commands
from discord.ext.commands import Bot
token = open("token.txt", 'r')

client = Bot(command_prefix=".")



client.run(token.read())