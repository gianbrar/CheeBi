import discord
import sys
import hashlib
import time
from discord.ext import commands
from discord.ext.commands import Bot

pingerslingerMaxPings = 50

replacementsList = [
    ["@here", "@herẹ"],
    ["@everyone", "@everyo̩ne"]
]
authUserHashes = [
  "2a1e72f48ec4b77d821be3243f6b5757ab0bd6a76c8ee07fe1091203f9ee4b9b87f1ed6feca3f403466c1d54dcd6165810ed1a98aba41674d8d4bcc8440320fd",
  "9f5ff27bae96e312e021d2e84b3ea04b47c59cd3e610b2d0be06fd141b61eb25b5e1c1c9343b4fe93a63fde20117de4f534218ac05f24bc0d7f7d0c30020f484"
]

slingerCooldown = []

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

#Help command:
@client.command()
async def help(ctx):
  await ctx.send("```CSS\nHi there! I'm CheeBi. Here's some of what I can do:\n.help: Show this message.\n.pingerslinger: Pings someone a certain amount of times with an optional custom message. (.pingerslinger -man for more information.)\n```")

#Ping(er)Sling(er) command:
@client.command()
async def pingsling(ctx):
  await allPing(ctx, False)
@client.command()
async def pingersling(ctx):
  await allPing(ctx, False)
@client.command()
async def pingslinger(ctx):
  await allPing(ctx, False)
@client.command()
async def pingerslinger(ctx):
  await allPing(ctx, False)


#Shutdown with authorization
@client.command()
async def shutdown(ctx):
  if hashlib.sha3_512(str(ctx.message.author.id).encode("utf-8")).hexdigest() in authUserHashes:
    await ctx.send("Shutting down & shutting up...")
    await client.logout()
  else:
    await ctx.send("You are not authorized to use that command.")



async def pingerSlinger(ctxIn, messageIn):
  try:
    uncleanArray = messageIn.content.split(" ")
    while("" in uncleanArray):
      uncleanArray.remove("")
    uncleanArray[2] = uncleanArray[2].split("\n")[0]
          
    if(uncleanArray[1] == "custom"):
      messageArray = messageIn.content.split("\n")
      messageArray.pop(0);
      for i in range(min(int(uncleanArray[2]), pingerslingerMaxPings)):
        await messageIn.channel.send(pingerslingerReplacements('\n'.join(messageArray)))
      if(uncleanArray[2] == "1"):
        conditionalRemoveS = 5;
      else:
        conditionalRemoveS = 6;
      
      await messageIn.channel.send(uncleanArray[2] + " pings"[0:conditionalRemoveS] + " sent graciously from " + messageIn.author.mention + ".")
      return
    
    for i in range(min(int(uncleanArray[2]), pingerslingerMaxPings)):
      await messageIn.channel.send(pingerslingerReplacements(uncleanArray[1]))

    if(uncleanArray[2] == "1"):
      conditionalRemoveS = 5;
    else:
      conditionalRemoveS = 6;

    await messageIn.channel.send(uncleanArray[2] + " pings"[0:conditionalRemoveS] + " sent graciously from " + messageIn.author.mention + ".")
  except:
    await allPing(ctxIn, True)

async def allPing(ctx, manual):
  if ctx.message.content[-3:] == "-man" or manual:
    await ctx.send("PINGERSLINGER FORMAT:```CSS\n.pingerslinger @CheeBi {however many times they are @ed}```\nor```CSS\n.pingerslinger custom {however many times message is sent}\n{custom message on this line}```")
    return
  await pingerSlinger(ctx, ctx.message)

def pingerslingerReplacements(stringIn):
    stringOut = stringIn
    for n in replacementsList:
        stringOut = stringOut.replace(n[0], n[1])
    return(stringOut)





client.run(token)