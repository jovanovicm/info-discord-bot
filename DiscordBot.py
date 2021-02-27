import discord
import asyncio
import re

import embeds
import keywords

client = discord.Client()
isActive = False


@client.event
async def on_message(message):
    global isActive
    if message.author == client.user:
        return

    if message.content == "-info":
        channel = message.channel
        if not isActive:
            await message.author.send('What do you want to know about?')

        if not isinstance(message.channel, discord.channel.DMChannel):
            await channel.send('Check your messages @{}'.format(message.author.name))

        def check(m):
            return m.author == message.author

        isActive = True

        while isActive:
            results = []
            c_list = []

            try:
                msg = await client.wait_for('message', check=check)
            except asyncio.TimeoutError:
                return

            s = msg.content
            s = re.sub(r'[^\w\s]', '', s)
            word_list = s.lower().split()

            for word in word_list:
                for kw_list in keywords.kw_lists:
                    if kw_list.__contains__(word):
                        kw_list[-1] += 1

            # correlation list
            for kw_list in keywords.kw_lists:
                c_list.append(kw_list[-1])
                kw_list[-1] = 0

            # max correlation value
            c_max_value = max(c_list)

            # keyword dictionary
            kw_dict = {
                'discord bot': {
                    'embed': embeds.embed1,
                    'correlation': c_list[0]
                },
                'discord bot 2': {
                    'embed': embeds.embed2,
                    'correlation': c_list[1]
                },
                'cv project': {
                    'embed': embeds.embed3,
                    'correlation': c_list[2]
                },
                'marko jovanovic': {
                    'embed': embeds.embed4,
                    'correlation': c_list[3]
                },
                'ishan kumar': {
                    'embed': embeds.embed5,
                    'correlation': c_list[4]
                },
                'iliana meco': {
                    'embed': embeds.embed6,
                    'correlation': c_list[5]
                }
            }

            for key, value in kw_dict.items():
                if value['correlation'] == c_max_value:
                    results.append(value['embed'])

            if c_max_value > 0:
                for embed in results:
                    await message.author.send(embed=embed)
            else:
                await message.author.send('No information found!')

    elif not isActive:
        await message.author.send('Start off by typing -info...')


# Events
@client.event
async def on_ready():
    print('ready to go!')

client.run('token')
