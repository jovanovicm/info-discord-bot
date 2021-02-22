import discord
import asyncio
import re

from discord.ext import commands

bot = commands.Bot(command_prefix='-', description="This is a Helper Bot")

#Discord Bot Project information
embed1=discord.Embed(title="Discord Bot Project", description="An introductory project that gets everyone up to pace with python and to spice up the discord!  We wanted to add some automation to the server as well as some fun games through means of a discord bot. ", color=0x42acae)
embed1.add_field(name="Starting Date", value="February 4th, 2021", inline=True)
embed1.add_field(name="Progress", value="Completed", inline=True)
embed1.set_footer(text="discord-bot")

discord_bot_keywords = ['discord', 'bot', 'project', 'february', 'projects', '2021', 'finished', 'done', 'completed', 'all', 'worked', 0]

#Discord Bot Project 2 information
embed2=discord.Embed(title="Discord Bot Project 2", description="An introductory project that gets everyone up to pace with python and to spice up the discord!  We wanted to add some automation to the server as well as some fun games through means of a discord bot. ", color=0x42acae)
embed2.add_field(name="Starting Date", value="February 4th, 2021", inline=True)
embed2.add_field(name="Progress", value="In Progress", inline=True)
embed2.set_footer(text="discord-bot-2")

discord_bot2_keywords = ['discord', 'bot', 'project', '2', 'february', 'projects', '2021', 'progress', 'all', 'now', 'current','currently', 0]

#Computer Vision Project information
embed3=discord.Embed(title="Computer Vision Project", description="Computer Vision Project", color=0x42acae)
embed3.add_field(name="Starting Date", value="March 2021", inline=True)
embed3.add_field(name="Progress", value="Planned", inline=True)
embed3.set_footer(text="computer-vision")

cv_keywords = ['computer', 'cv', 'vision', 'project', 'march', 'projects', '2021', 'planned', 'all', 'soon', 'future', 'next', 0]

kw_lists = [discord_bot_keywords, discord_bot2_keywords, cv_keywords]

@bot.event
async def on_message(message):
  if message.content == "-project info":
    channel = message.channel
    await channel.send('What project(s) do you want to know about?')

    def check(m):
      return m.author == message.author and m.channel == message.channel

    try:
      msg = await bot.wait_for('message', check=check, timeout=30.0)
    except asyncio.TimeoutError:
      return await channel.send('`timed out`')


    s = msg.content
    s = re.sub(r'[^\w\s]','',s)
    word_list = s.lower().split()

    for word in word_list:
      for kw_list in kw_lists:
        if kw_list.__contains__(word):
          kw_list[-1] += 1
        
    #correlation list
    c_list = []
    for kw_list in kw_lists:
      c_list.append(kw_list[-1])
      kw_list[-1] = 0
    
    #max correlation value
    c_max_value = max(c_list)

    kw_dict = {
      'discord bot': {
      'embed' : embed1,
      'correlation' : c_list[0]
        },
      'discord bot 2': {
      'embed' : embed2,
      'correlation' : c_list[1]
        },
      'cv project': {
      'embed' : embed3,
      'correlation' : c_list[2]
       }
    }

    results = []
    for key,value in kw_dict.items():
      if value['correlation'] == c_max_value:
        results.append(value['embed'])

    if c_max_value > 1:
      for embed in results:
        await message.channel.send(embed = embed)
    else:
      await message.channel.send('No projects found!')
    
# Events
@bot.event
async def on_ready():
  print('ready to go!')

bot.run('token')
