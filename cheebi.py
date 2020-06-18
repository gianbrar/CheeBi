import discord
import json
import sys
import hashlib
import time
import asyncio
from discord.ext import commands
from discord.ext.commands import Bot

cleanupVar = False

pingerslingerMaxPings = 50



replacementsList = [
    ["@here", "@herẹ"],
    ["@everyone", "@everyo̩ne"]
]

announcementList = {
}



authUserHashes = [
  "2a1e72f48ec4b77d821be3243f6b5757ab0bd6a76c8ee07fe1091203f9ee4b9b87f1ed6feca3f403466c1d54dcd6165810ed1a98aba41674d8d4bcc8440320fd",
  "9f5ff27bae96e312e021d2e84b3ea04b47c59cd3e610b2d0be06fd141b61eb25b5e1c1c9343b4fe93a63fde20117de4f534218ac05f24bc0d7f7d0c30020f484"
]

slingerCooldownSeconds = 30
slingerCooldownUsers = []


#Define classes

class slingerUser:
  def __init__(self, ID, cooldownTime):
    self.ID = ID
    self.cooldownTime = cooldownTime
  def cooldownTrim(self, currentTime):
    return currentTime - self.cooldownTime >= slingerCooldownSeconds

class announcement:
  def __init__(self, announceTime, announceText):
    self.UTCTime = announceTime
    self.text = announceText
   


#Discord.py setup & get token
client = Bot(command_prefix=".")
client.remove_command("help")

if len(sys.argv) > 1:
  if not sys.argv[1].startswith("-"):
    token = sys.argv[1]
  else:
    token = open("token.txt", 'r').read().split("\n")
    if sys.argv[len(sys.argv) - 1] == "-dev":
      token = token[0]
    elif sys.argv[len(sys.argv) - 1] == "-pub":
      token = token[1]
else:
  if token.find("\n") == -1:
    token = open("token.txt", 'r').read()
  else:
    token = open("token.txt", 'r').read()
    token = token[:token.find("\n")]



@client.event
async def on_ready():
  print("CheeBi activated at " + time.asctime(time.localtime(time.time())))
  await client.change_presence(status=discord.Status.online, activity=discord.Game(name='.help'))
  await trimCooldowns()

#Help command:
@client.command()
async def help(ctx):
  await ctx.send("```CSS\nHi there! I'm CheeBi. Here's some of what I can do:\n.help: Show this message.\n.pingerslinger: Pings someone a certain amount of times with an optional custom message. (.pingerslinger -man for more information.)\n.announce: Schedules an announcement. (.announce -man for more information)```")

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

#Announcement
@client.command()
async def announce(ctx):
  if ctx.message.content[-4:] == "-man":
    await ctx.send("ANNOUNCEMENT FORMAT:```CSS\nTo announce in certain amount of time, use the format:\n\n.announce in (_w)(_d)(_h)(_m)(_s) to {your group goes here} message:\n{YOUR ANNOUNCEMENT GOES HERE}\n\n\nTo announce at a specific time, (based by default on the server's timezone), use the format:\n\n.announce at (month)(date)(hour)(time)```")
    return
  if ctx.message.author.guild_permissions.mention_everyone:
    await ctx.send("@everyone, hey, this person is an idiot!")
  else:
    await ctx.send("You are not authorized to use that command.")

#Shutdown with authorization
@client.command()
async def shutdown(ctx):
  if authuser(ctx.message.author.id):
    await ctx.send("Shutting down & shutting up...")
    await client.logout()
  else:
    await ctx.send("You are not authorized to use that command.")



async def pingerSlinger(ctxIn, messageIn):
  userCooldownComplete = slingerCooldownDone(messageIn.author.id)

  
  if not userCooldownComplete[0]:
    await ctxIn.send(messageIn.author.mention + ", you cannot use the pingerslinger command for another: " + str(timeLeft(userCooldownComplete[1])) + " seconds.")
    return
  try:
    slingerCooldownUsers.append(slingerUser(messageIn.author.id, int(time.time())))
    slingerindex = len(slingerCooldownUsers)
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
    slingerCooldownUsers.append(slingerUser(messageIn.author.id, int(time.time())))
  except:
    await allPing(ctxIn, True)

async def allPing(ctx, manual):
  if ctx.message.content[-4:] == "-man" or manual:
    await ctx.send("PINGERSLINGER FORMAT:```CSS\nFormat to @ someone a certain number of times:\n.pingerslinger @CheeBi {however many times they are @ed}```\nor```CSS\nFormat to send a custom message a certain number of times:\n.pingerslinger custom {however many times message is sent}\n{custom message on this line}```")
    return
  await pingerSlinger(ctx, ctx.message)

def pingerslingerReplacements(stringIn):
    stringOut = stringIn
    for n in replacementsList:
        stringOut = stringOut.replace(n[0], n[1])
    return(stringOut)


async def trimCooldowns():
  await asyncio.sleep(120)

async def announceLoop():
  global cleanupVar
  while not cleanupVar:
    await ayncio.sleep(5)

async def returnAnnounceObject(announcementString):
  keywordArray = announcementString.content.split(" ")
  while "" in keywordArray:
    keywordArray.remove("")
  if keywordArray[1] == "in":
    print("announce in")
  elif keywordArray[1] == "at":
    print("announce at")

def slingerCooldownDone(userID2Check):
  global slingerCooldownUsers
  timeOfMessage = int(time.time())
  for i in slingerCooldownUsers:
    if userID2Check == i.ID:
      if not i.cooldownTrim(timeOfMessage):
        return [False, i.cooldownTime]
  return [True, 0]

def timeLeft(timeIn):
  return(timeIn - int(time.time()) + slingerCooldownSeconds)

def authuser(userID):
  return hashlib.sha3_512(str(userID).encode("utf-8")).hexdigest() in authUserHashes


client.run(token)