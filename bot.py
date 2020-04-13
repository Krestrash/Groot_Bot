import json
import random
import requests
import shutil
import os
from PIL import Image, ImageFont, ImageDraw
import discord
import discord.utils

path = os.path.dirname(os.path.realpath(__file__))

channel = 465232155992260611
allow_txt_chanels = ['465232155992260611']
PREF = '.'
TOKEN = ''
client = discord.Client()


async def show_lvl(message, users):
    ava = f"https://cdn.discordapp.com/avatars/{message.author.id}/{message.author.avatar}.png?size=1024"
    resp = requests.get(ava, stream=True)
    local_file = open(path + '\\tmp\\' + str(message.author.id) + '.png', 'wb')
    resp.raw.decode_content = True
    shutil.copyfileobj(resp.raw, local_file)

    exp = users[str(message.author.id)]['exp']
    lvl = users[str(message.author.id)]['lvl']

    im1 = Image.open(path + '\\imgsets\\l10.png')
    im2 = Image.open(path + f'\\tmp\\{message.author.id}.png')
    im2 = im2.resize((160, 160), Image.ANTIALIAS)
    im3 = Image.open(path + '\\imgsets\\l1.png')
    dst = Image.new('RGBA', (720, 217))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (22, 26))
    dst.save(path + '\\tmp\\tmp.png')
    img = Image.open(path + '\\tmp\\tmp.png').convert("RGBA")
    dst = ImageDraw.Draw(img)
    # (194, 132), (697, 184)
    # 503
    x = int(((lvl + 1) / 0.7) ** 4)
    rx = int((503 / x) * exp)
    dst.rectangle(((194, 132), (rx + 194, 184)), fill='white')
    dst = Image.new('RGBA', (720, 217))
    dst.paste(img, (0, 0), im3)
    dst.save(path + '\\tmp\\tmp.png')

    img = Image.open(path + '\\imgsets\\l0.png')
    im1 = Image.open(path + '\\tmp\\tmp.png')
    dst = Image.new('RGBA', (720, 217))
    dst.paste(img, (0, 0))
    dst.paste(im1, (0, 0), mask=im1)
    dst.save(path + '\\tmp\\tmp.png')

    img = Image.open(path + '\\tmp\\tmp.png').convert("RGBA")
    dst = ImageDraw.Draw(img)
    font = ImageFont.truetype(path + '\\font.ttf', 36)
    text = message.author.name
    dst.text((200, 95), text, font=font, fill=(255, 255, 255, 255))

    font = ImageFont.truetype(path + '\\font.ttf', 20)
    text = '#' + message.author.discriminator
    dst.text((200, 70), text, font=font, fill=(255, 255, 255, 255))

    font = ImageFont.truetype(path + '\\font.ttf', 20)
    text = f'{exp}/{x}'
    w = font.getmask(text).getbbox()
    wi = img.size[0]
    dst.text((wi - (w[2] + 10), 110), text, font=font, fill=(150, 150, 150, 255))

    font = ImageFont.truetype(path + '\\font.ttf', 40)
    font1 = ImageFont.truetype(path + '\\font.ttf', 20)
    text = ' ' + str(users[str(message.author.id)]['lvl'])
    text1 = '      lvl.  ' + (' ' * len(text))
    text2 = ' #' + str(users[str(message.author.id)]['rank']) + '  '
    text3 = 'rank  ' + (' ' * len(text))
    w1 = font.getmask(text).getbbox()
    w2 = font1.getmask(text1).getbbox()
    w3 = font.getmask(text2).getbbox()
    w4 = font1.getmask(text3).getbbox()
    wi = img.size[0]
    y = 25
    dst.text((wi - (w1[2] + 10), y), text, font=font, fill=(255, 255, 255, 255))
    dst.text((wi - (w2[2] + 10 + w1[2]), y + 20), text1, font=font1, fill=(255, 255, 255, 255))
    dst.text((wi - (w3[2] + 10 + w1[2] + w2[2]), y), text2, font=font, fill=(255, 255, 255, 255))
    dst.text((wi - (w4[2] + 10 + w1[2] + w2[2] + w3[2]), y + 20), text3, font=font1, fill=(255, 255, 255, 255))
    img.save(path + '\\tmp\\tmp.png')
    chanel = client.get_channel(channel)
    await chanel.send(file=discord.File(path + '\\tmp\\tmp.png'))


async def update_data(users, message):
    if str(message.author.id) not in users:
        users[str(message.author.id)] = {}
        users[str(message.author.id)]['exp'] = 0
        users[str(message.author.id)]['lvl'] = 0
        users[str(message.author.id)]['rank'] = 0


async def add_experiece(users, message, exp):
    if message.content.startswith != PREF:
        users[str(message.author.id)]['exp'] += exp
        tmp = {}
        for i in users:
            tmp[i] = users[i]


async def ranking(users):
    tmp = {}
    for i in users:
        tmp[i] = users[i]['exp']

    a = 1
    for i in tmp:
        users[i]['rank'] = a
        a += 1
    with open('users.json', 'w') as f:
        json.dump(users, f)

async def level_up(users, message):
    exp = users[str(message.author.id)]['exp']
    lvl_start = users[str(message.author.id)]['lvl']
    lvl_end = int(0.7 * exp ** (1 / 4))
    msg = [f'Поздравляю! {str(message.author.mention)}, у тебя новый lvl {str(lvl_end)}!']
    if lvl_start < lvl_end:
        chanel = client.get_channel(channel)
        await chanel.send(str(random.choice(msg)))
        users[str(message.author.id)]['lvl'] = lvl_end
    await ranking(users)


async def cmds(message, users):
    if message.content == PREF + 'lvl':
        await show_lvl(message, users)


@client.event
async def on_ready():
    print('LvlBot started\n------------------------')
    print(client.user)
    print(client.user.id)
    print('------------------------')


@client.event
async def on_member_join(member):
    with open('users.json', 'r') as f:
        users = json.load(f)

    if str(member.id) not in users:
        users[str(member.id)] = {}
        users[str(member.id)]['exp'] = 0
        users[str(member.id)]['lvl'] = 0

    role = discord.utils.get(member.server.roles, name = '')

    with open('users.json', 'w') as f:
        json.dump(users, f)


@client.event
async def on_message(message):
    if not message.author.bot:
        with open('users.json', 'r') as f:
            users = json.load(f)
        print(message)
        print(message.content)

        if (message.content != '') \
                and (message.content.startswith != PREF) \
                and (message.channel.id not in allow_txt_chanels):

            await update_data(users, message)
            await add_experiece(users, message, random.randint(5, 15))
            await level_up(users, message)
            print(f'content = {message.content}; lvl = {users[str(message.author.id)]["lvl"]}; exp = {users[str(message.author.id)]["exp"]}; author = {message.author}; rank = {users[str(message.author.id)]["rank"]}')

        await cmds(message, users)

        with open('users.json', 'w') as f:
            json.dump(users, f)


client.run(TOKEN)
