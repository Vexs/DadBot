#!/usr/bin/env python3
import discord
from discord.ext import commands
import re

from tokenfile import TOKEN

bot = commands.Bot(command_prefix='>>')


@bot.event
async def on_message(message):
    await dadjoke(message)
    await bot.process_commands(message)


@bot.event
async def on_ready():
    print('Bot ready!')
    print('Logged in as ' + bot.user.name)
    print('-------')


@bot.event
async def on_server_join(ser):
    await bot.send_message(ser.default_channel, 'Hi {}, I\'m DadBot!'.format(ser.name))
    if not ser.me.server_permissions.manage_nicknames:
        await bot.send_message(ser.default_channel,
                               'Unfortunately kiddo, I need to be able to give you a nick! '
                               'Invite me back with that permission!\n'
                               'https://discordapp.com/oauth2/authorize?client_id=284941193714860032&scope=bot&permissions=201329664')
        await bot.leave_server(ser)


async def dadjoke(message):
    if message.author != message.server.me and message.author.top_role < message.server.me.top_role:
        word = re.search(r'\bi\'?m\s+(.*)', message.content, re.IGNORECASE)
        if word is not None:
            if len(word.group(1)) > 32:
                word = re.search(r'\bi\'?m\s+(\w+)', message.content, re.IGNORECASE)
            word = word.group(1)
            if message.server.me.server_permissions.manage_nicknames:
                if len(word) > 32:
                    word = '<LONG DADJOKE>'
                await bot.change_nickname(message.author, word)
                await bot.send_message(message.channel, 'Hi {}, I\'m dad!'.format(word))
            else:
                await bot.send_message(message.server.default_channel,
                                       'Hey! Who stole my pencil! I can\'t nick anyone!')


bot.run(TOKEN, bot=True)
