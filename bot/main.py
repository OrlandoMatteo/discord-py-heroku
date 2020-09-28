import os

import discord
import json
client = discord.Client()

TOKEN = os.getenv('DISCORD_TOKEN')
ADMIN=os.getenv('ADMIN')
#backup=json.load(open("backupQueue.json"))
backup={"queue": []}
def isAdmin(user):
    return user==ADMIN



@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$askHelp'):
        backup["queue"].append({"author":str(message.author),"id":message.author.mention})
        json.dump(backup,open("backupQueue.json","w"))
     
        await message.channel.send("you've been added to the queue type $show to view it")

    if message.content.startswith('$show'):
        j=json.load(open("backupQueue.json"))
        textMessage="**Queue** ```Markdown\n \n"
        for i,item in enumerate(backup["queue"]):         
            textMessage+=str(i)+". "+item["author"]+"\n"
        textMessage+="```"
        await message.channel.send(textMessage)

    if "$" not in message.content:
        await message.delete()

    if message.content.startswith("$clear") and isAdmin(str(message.author)):
        tmp = await message.channel.send('Clearing messages...')
        async for msg in message.channel.history()[:-2]:
            await msg.delete()
        backup["queue"]=[]
        #json.dump(backup,open("backupQueue.json","w"))

    if message.content.startswith("$next") and isAdmin(str(message.author)):
        backup["queue"].pop(0)
        await message.channel.send(backup["queue"][0]["id"]+" It is your turn now 👍")
        #json.dump(backup,open("backupQueue.json","w"))


client.run(TOKEN)