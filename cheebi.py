import discord
import json
import sys
import os
import hashlib
import time
import asyncio
from discord.ext import commands
from discord.ext.commands import Bot





"""
These are the declarations of all the variables, lists, objects, classes, etc. used in Cheebi.
"""



"""These are variables, lists, etc. used by multiple commands and functions."""

#This variable is used to signal to other threads when the program is closing.
cleanupVar = False

#These are the SHA-3 512 hashes of the User IDs of the users authorised to administer the bot.
authUserHashes = [
  "2a1e72f48ec4b77d821be3243f6b5757ab0bd6a76c8ee07fe1091203f9ee4b9b87f1ed6feca3f403466c1d54dcd6165810ed1a98aba41674d8d4bcc8440320fd",
  "9f5ff27bae96e312e021d2e84b3ea04b47c59cd3e610b2d0be06fd141b61eb25b5e1c1c9343b4fe93a63fde20117de4f534218ac05f24bc0d7f7d0c30020f484"
]



"""These are variables used by the announce command (and it's functions)"""

#This list is used to store what announcements will need to be sent in the future.
announcementList = [
]



"""These are variables used by the ping(er)Sling(er) command (and it's functions)"""

#This variable sets how long it is before a user can send another ping(er)Sling(er) command after one is sent.
slingerCooldownSeconds = 30

#This list stores what users have a cooldown period and the time at which their last pingerslinger command was sent.
slingerCooldownUsers = []

#This is the makimum number of pings allowed in a ping(er)Sling(er) single command.
pingerslingerMaxPings = 50

#This is the list of replacements that the pingerSlinger will perform on it's custom strings.
replacementsList = [
    ["@here", "@herẹ"],
    ["@everyone", "@everyo̩ne"]
]



"""These are the definitions of all the classes used in Cheebi."""

#Class for the pingerSlinger's user cooldowns.
class slingerUser:
  def __init__(self, ID, cooldownTimestamp):
    self.ID = ID
    self.cooldownTimestamp = cooldownTimestamp
  def cooldownTrim(self, currentTime):
    return currentTime - self.cooldownTimestamp >= slingerCooldownSeconds

#Class for announcement users cooldowns.
class announcement:
  def __init__(self, announceTime, announceText, userID):
    self.UTCTime = announceTime
    self.text = announceText
    self.iD = userID
   


#Discord.py setup & get token
prefix = "."
if len(sys.argv) > 1:
  if not sys.argv[1].startswith("-"):
    token = sys.argv[1]
    print(hashlib.sha3_512(token.encode("utf-8")).hexdigest())
    if hashlib.sha3_512(token.encode("utf-8")).hexdigest() == "45659ae3ce89a83d08393f57129c05c03083c2ec9ac31c80a9b09b50acb8ef6b0898edf7f3586b58c7e7d5311d0a9cba09e3ccaa51196aaad3681a4bc7902f39":
      prefix = "~~"
  else:
    token = open("token.txt", 'r').read().split("\n")
    if sys.argv[len(sys.argv) - 1] == "-dev":
      token = token[0]
      prefix = "~~"
    elif sys.argv[len(sys.argv) - 1] == "-pub":
      token = token[1]
else:
  if token.find("\n") == -1:
    token = open("token.txt", 'r').read()
  else:
    token = open("token.txt", 'r').read()
    token = token[token.find("\n"):]

client = Bot(command_prefix=prefix)
client.remove_command("help")





"""
This is the beginning of the declarations of bot commands. Each of the command functions have their own set of functions and parsers.
"""



#Begin
@client.event
async def on_ready():
  print("CheeBi activated at " + time.asctime(time.localtime(time.time())))
  await client.change_presence(status=discord.Status.online, activity=discord.Game(name='.help'))
  """asyncio.create_task(
    trimCooldowns()
  )
  asyncio.create_task(
    announceLoop()
  )"""



#Help command:
@client.command()
async def help(ctx):
  global prefix
  await ctx.send("```CSS\nHi there! I'm CheeBi. Here's some of what I can do:\n" + prefix + "help: Shows this message.\n" + prefix + "pingerslinger: Pings someone a certain amount of times with an optional custom message. (" + prefix + "pingerslinger -man for more information.)\n" + prefix + "announce: Schedules an announcement. (" + prefix + "announce -man for more information)```")



#Ping(er)Sling(er) command(s):
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

#Announcement command:
@client.command()
async def announce(ctx):
  global prefix
  #Manual page:
  if ctx.message.content[len(prefix)+9:].strip().lower() == "-man":
    await ctx.send("ANNOUNCEMENT FORMAT:```CSS\nTo announce in certain amount of time, use the format:\n\n" + prefix + "announce in (_w)(_d)(_h)(_m)(_s)* to {target group/user with/without the @ symbol} (inchannel #_____) (-discreet) message:\n{your announcement message goes here}\n\n\nTo announce at a specific time, (based by default on the server's timezone), use the format:\n\n" + prefix + "announce at (month)* (day number)* (hour)* (minute)* (tz {three letter time zone code}) to {target group/user with/without the @ symbol} (inchannel #_____) (-discreet) message:\n{your announcement message goes here}\n\n\nAnything in parenthesis () is optional, and anything in braces {} is a description of what goes there.\n*Although all of these are marked as optional, at least one is required```")
    return
  elif ctx.message.content[len(prefix)+9:].strip().lower() == "-discreet":
    
  #Setchannel commands:
  elif ctx.message.content[len(prefix)+8:len(prefix)+20].strip().lower() == "setchannel":
    nextCommandPart = ctx.message.content.find("setchannel")+10
    if  (ctx.message.content[nextCommandPart:].strip() == "-man"):
      await ctx.send("There probably should be a manual here.")
    elif(ctx.message.content[nextCommandPart:].strip() == "remove"):
      await ctx.send("(Non-existent) Channel macro removed.")

    else:
      await ctx.send("Channel macro (not actually) set to \"" + ctx.message.content[21:].strip().split("\n")[0] + "\".")

  #Get announce object
  elif ctx.message.author.guild_permissions.mention_everyone:
    announcementList.append(await returnAnnounceObject(ctx.message.content, ctx.message))
  
  #Insufficient authorization, handler:
  else:
    await ctx.send("You are not authorized to use that command.")



#Shutdown command with authorization:
@client.command()
async def shutdown(ctx):
  if authuser(ctx.message.author.id):
    await ctx.send("Shutting down & shutting up...")
    await client.logout()
    print("CheeBi stopped at " + time.asctime(time.localtime(time.time())))
  else:
    await ctx.send("You are not authorized to use that command.")


#Restart command with authorization:
@client.command()
async def restart(ctx):
  if authuser(ctx.message.author.id):
    await ctx.send("Restarting & reworking...")
    await client.logout()
    print("CheeBi restarted at " + time.asctime(time.localtime(time.time())))
    os.execv(sys.executable, ['python3'] + sys.argv)
  else:
    await ctx.send("You are not authorized to use that command.")

"""
This is the beginning of the helper functions for the bot commands. These have a range of functionality from doing all of the work for the command to doing a miniscule task for a specific part of a command.
"""



"""These are the ping(er)Sling(er) command helper functions."""

#This function almost fully handles all of the functionality of pingerSlinger. The manual is handled by the lower function.
async def pingerSlinger(ctxIn, messageIn):
  userCooldownComplete = slingerCooldownDone(messageIn.author.id)
  if not userCooldownComplete[0]:
    await ctxIn.send(messageIn.author.mention + ", you cannot use the pingerslinger command for another: " + str(timeLeft(userCooldownComplete[1]), slingerCooldownSeconds) + " seconds.")
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
  

  except: await allPing(ctxIn, True)

#Handles the ping(er)Sling(er) manual and runs the pingerSlinger command (if applicable).
async def allPing(ctx, manual):
  if ctx.message.content[-4:] == "-man" or manual:
    await ctx.send("PINGERSLINGER FORMAT:```CSS\nFormat to @ someone a certain number of times:\n" + prefix + "pingerslinger @CheeBi {however many times they are @ed}```\nor```CSS\nFormat to send a custom message a certain number of times:\n" + prefix + "pingerslinger custom {however many times message is sent}\n{custom message on this line}```")
    return
  await pingerSlinger(ctx, ctx.message)



#This removes all pings to @everyone and @here for the ping(er)Sling(er) and replaces them with a similar string. (For example, @everyone -> @everyo̩ne.) These replacements may or may not be expanded upon in the future.
def pingerslingerReplacements(stringIn):
    stringOut = stringIn
    for n in replacementsList:
        stringOut = stringOut.replace(n[0], n[1])
    return(stringOut)



#This function checks if a user by a given ID is allowed to send another ping(er)Sling(er) command. Otherwise it tells them their cooldown time left.
def slingerCooldownDone(userID2Check):
  global slingerCooldownUsers
  timeOfMessage = int(time.time())
  slingerUserObj = next((i for i in slingerCooldownUsers if i.ID == userID2Check), None)
  try:
    if not slingerUserObj.cooldownTrim(timeOfMessage):
      return [False, slingerUserObj.cooldownTimestamp]
    return [True, 0]
  except:
    return [True, 0]


#This is a WIP command to lower the length of the cooldown arrays. (Reducing the size of the JSON file.) It runs about every 2 minutes.
async def trimCooldowns():
  await asyncio.sleep(120)



"""These are the announce command helper functions."""

#This is a WIP command that actually sends the announcements when they are ready. This is version 1 of the command. This will later be split into two commands, one which keeps the list sorted by UTC timestamp, (via insertion,) and one who more efficiently runs through the list of announcments chronologically. (This likely will also implement a full sort every 5-10 minutes to prevent from errors building up.)
async def announceLoop(message):
  global cleanupVar
  while not cleanupVar:
    await asyncio.sleep(30)
    for currAnnouncement in announcementList:
      if currAnnouncement.announceTime():
        currAnnouncement.announce()
        announcementList.remove(currAnnouncement)
        announcementList[str(message.guild.id)][str(message.user.id)] -= 1



#This parses any actual announcements from the "announce" command. It returns an "announcement" object.
async def returnAnnounceObject(announcementString, messageObj):
  keywordArray = announcementString.split(" ")
  while "" in keywordArray:
    keywordArray.remove("")

  indexOf_to_ = keywordArray.index("to")
  announcementSubjectIndex = announcementString.find(keywordArray[indexOf_to_])
  announcementSubjectIndex += announcementString[announcementSubjectIndex:].find(keywordArray[indexOf_to_ + 1])

  
  afterNameIndex = -1

  tokenIndex = announcementSubjectIndex
  for token in keywordArray:
    afterNameIndex += 1
    tokenIndex += announcementString[tokenIndex:].find(token)
    if token == "inchannel" or token == "message:":
      noError = True
      break


  subjectName = announcementString[announcementSubjectIndex:tokenIndex].strip()
  if subjectName.startswith("<@!"):
    subjectToAnnounceMention = subjectName
  else:
    subjectToAnnounceTo = getRoleByName(subjectName, messageObj.guild)
    if subjectToAnnounceTo == None:
      subjectToAnnounceTo = getUserByName(subjectName, messageObj.guild)
      if subjectToAnnounceTo[0] == None:
        await messageObj.channel.send("There is no role or user named \"" + subjectName + "\".")
        return None
      elif subjectToAnnounceTo[1] == True:
        await messageObj.channel.send("\nThere are multiple users in this server under the name of \"" + subjectName + "\". Please include the Discord Tag. (EG: username#1234)")
        return None
    subjectToAnnounceMention = subjectToAnnounceTo[0].mention
  
  timeUntilDict = {"w":604800, "d":86400, "h":3600, "m":60, "s":1}
  timeUntil = 0
  if keywordArray[1] == "in":
    for i in timeUntilDict.keys():
      j = keywordArray[2].find(i) - 1
      if not j == -2:
        unit = ""
        while keywordArray[2][j] not in timeUntilDict.keys():
          unit = keywordArray[2][j] + unit
          if j == 0:
            break
          j -= 1
        timeUntil += int(unit) * timeUntilDict[i]
    await messageObj.channel.send(str(timeUntil) + " seconds until the announcement.")
  elif keywordArray[1] == "at":
    print("announce at")
  await messageObj.channel.send("Subject is: " + subjectToAnnounceMention)



#This function gets the relevant guild's role by its name.
def getRoleByName(roleName, guildObj):
  return next((roleObj for roleObj in guildObj.roles if roleObj.name == roleName), None)

#This function gets the user by their name.
def getUserByName(userName, guildObj):
  if userName.find("#") == -1:
    multiMem = False
    outputMem = None
    for membObj in guildObj.members:
      if membObj.name == userName or membObj.display_name == userName:
        multiMem = not outputMem == None # what even is this
        outputMem = membObj
    return [outputMem, multiMem]
  else:
    return [next((membObj for membObj in guildObj.members if membObj.name + "#" + membObj.discriminator == userName or membObj.display_name + "#" + membObj.discriminator == userName), None), False]



"""These are general functions used by multiple commands"""

#This function takes a UTC timestamp and a cooldown length (in seconds)) and calculates the time left in the cooldown.
def timeLeft(timeIn, cooldownTime):
  return(timeIn - int(time.time()) + cooldownTime)



#This function checks if the user is allowed to manage the bot. 
def authuser(userID):
  return hashlib.sha3_512(str(userID).encode("utf-8")).hexdigest() in authUserHashes
  
    



"""
And finally, everybody's favorite command. The one that sets off the discord bot. The highly worshipped client.run().
"""
client.run(token)

