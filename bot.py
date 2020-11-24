#!/usr/bin/python3
# bot.py
import os
import random
import re
import discord
from dotenv import load_dotenv
import unicodedata

def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
FILE = os.getenv('LIST_FILE')
MC_FILE = os.getenv('MC_LIST_FILE')

client = discord.Client()

with open(FILE, "r", encoding='utf-8') as f:
    liste = set(s.strip() for s in f.readlines())
    lower = set(remove_accents(l.lower()) for l in liste)

with open(MC_FILE, "r", encoding='utf-8') as f:
    pseudos = set(p.strip() for p in f.readlines())

@client.event
async def on_ready():
    kw = len(liste)
    print(f'{client.user} has connected to Discord with {kw} keywords!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.lower() == "servalist":
        await message.channel.send('\n'.join(liste))
    else:
        unformated = remove_accents(message.content.lower())

        if bool(re.match(r"^servadd (.*)?$", unformated)):
            add = " ".join(message.content.split()[1:])
            unformated = remove_accents(add.lower())
            if bool(re.match(r"^S[eE][rR][vV][aA][lL][A-Za-z0-9\'_-]+", remove_accents(add))):
                liste.add(add)
                lower.add(unformated)
                with open(FILE, 'a') as f:
                    f.write(add+"\n")
                await message.channel.send(add+" added!")
            else:
                await message.channel.send(add+" is invalid!")
        if bool(re.match(r"^serval[a-z0-9\'_-]+", unformated)):
            response = random.choice(list(liste))
            await message.channel.send(response)
        if bool(re.match(r".*(serval|lavres|bg).*", unformated)):
            await message.add_reaction("❤️")
        if bool(re.match(r"^([\s\S]* )?(keut|hugo|21|keutar|keuts)( [\s\S]*)?$", unformated)):
            await message.add_reaction("<:21:649012488863744016>")
        if bool(re.match(r"^([\s\S]* )?(man|timo|timothee|rtf\w+)( [\s\S]*)?$", unformated)):
            await message.add_reaction("<:aroufmmh:649013248011665408>")
        if bool(re.match(r"^([\s\S]* )?acu( [\s\S]*)?$", unformated)):
            await message.add_reaction("<:kawai:649018159948627970>")
        if bool(re.match(r"^([\s\S]* )?flex( [\s\S]*)?$", unformated)):
            await message.add_reaction("💯")
        if bool(re.match(r"^([\s\S]* )?rose( [\s\S]*)?$", unformated)):
            await message.add_reaction("<:sjw:649015036622405655>")
        if bool(re.match(r"^([\s\S]* )?vikings?( [\s\S]*)?$", unformated)):
            await message.add_reaction("<:viking:777909531187216394>")
        if bool(re.match(r".*`{3}[^`]*`{3}.*", unformated)):
            if bool(re.match(r".*`{3}c\s[^`]*`{3}.*", unformated)):
                await message.channel.send("FLAG TRICHE !! <@!179881648098246656>")
            else:
                await message.channel.send("FLAG TRICHE !!")
            await message.add_reaction("<:tatamireza:649010752342065153>")
        if bool(re.match(r"^mcpseudo$", unformated)):
            await message.channel.send("/rg addmember region pseudo\n"+"\n".join(pseudos))
        if bool(re.match(r"^mcpseudo (.*)$", unformated)):
            add = " ".join(message.content.split()[1:])
            pseudos.add(add)
            with open(MC_FILE, 'a') as f:
                f.write(add+"\n")
            await message.channel.send("Mcpseudo: '" + add + "' added!");

client.run(TOKEN)
