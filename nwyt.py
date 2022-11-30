import discord
from discord.utils import get
from discord import Webhook, AsyncWebhookAdapter
import aiohttp

client=discord.Client(intents=discord.Intents.all())

@client.event
async def on_ready():
    print('r')
    await client.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name='people type 👀'))
    
@client.event
async def on_typing(channel, user, when):
    if channel.guild.id == 913268801599078471:
        await client.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name=f"{user.display_name}#{user.discriminator} 👀"))    

@client.event
async def on_message(m):
    if (m.author.id == 437808476106784770 or m.author.id == 318259292820078592) and m.channel.id == 913436481429835796 and len(m.content) > 15:

        mem = m.mentions[0]
        lvl = int(m.content.split()[5].replace('*',''))
        coastguard = 925447689213194353
        cruiser = 925447687183142973
        destroyer = 925447684515590155
        submarine = 925447681533423627
        carrier = 925447664907210802

        if lvl == 80:
            await mem.add_roles(get(m.guild.roles, id=carrier))
            await mem.remove_roles(get(m.guild.roles, id=submarine))
            await m.add_reaction(emoji='✅')
        elif lvl == 45:
            await mem.add_roles(get(m.guild.roles, id=submarine))
            await mem.remove_roles(get(m.guild.roles, id=destroyer))
            await m.add_reaction(emoji='✅')            
        elif lvl == 30:
            await mem.add_roles(get(m.guild.roles, id=destroyer))
            await mem.remove_roles(get(m.guild.roles, id=cruiser))
            await m.add_reaction(emoji='✅')
        elif lvl == 15:
            await mem.add_roles(get(m.guild.roles, id=cruiser))
            await mem.remove_roles(get(m.guild.roles, id=coastguard))
            await m.add_reaction(emoji='✅')
        elif lvl == 8:
            await mem.add_roles(get(m.guild.roles, id=coastguard))
            await m.add_reaction(emoji='✅')
        else:
            await m.add_reaction(emoji='☑️')

    if m.content.split(' ')[0] == '.rr' and (m.author.id == 140902977618706432 or m.author.id == 318259292820078592 or m.author.id == 426451069560946698): #DM REPLIES
        try:
            uid = int(m.content.split(' ')[1])
            mcont = m.content[23:]
            usr = None
            for g in client.guilds:
                if usr is None:
                    usr = g.get_member(uid)
            if not usr is None:
                await usr.create_dm()
                try:
                    await usr.dm_channel.send(mcont)
                    await m.add_reaction(emoji='✅')
                except Exception as e:
                    await m.reply(e)
                    await m.add_reaction(emoji='🚫')
            else:
                try:
                    await client.get_channel(uid).send(mcont)
                    await m.add_reaction(emoji='✅')
                except Exception as e:
                    await m.reply(e)
                    await m.add_reaction(emoji='🚫')
        except Exception as e:
            await m.reply(e)
            await m.add_reaction(emoji='🚫')
            return

    if m.content.split(' ')[0] == '.an':
        if (await client.get_guild(913268801599078471).fetch_member(m.author.id)).guild_permissions.manage_guild == True or m.author.id == 140902977618706432:
            dat = open('NWYTbl','r').read().split()
            dat.append((m.content.split(' ')[1]).lower())
            f=open('NWYTbl','w')
            f.write(str(" ".join(dat)))
            f.close()
            mc = 0
            for mem in m.guild.members:
                mc+=1
                for e in dat:
                    if e in str(mem.name.lower()) or e in str(mem.display_name.lower()):
                        print('y')
                        if not mem.guild_permissions.administrator:
                            await mem.edit(nick='')
            print('Done')

    if m.content.split(' ')[0] == '.ruleupdate':
        if (await client.get_guild(913268801599078471).fetch_member(m.author.id)).guild_permissions.manage_guild == True or m.author.id == 140902977618706432:
            msg = await client.get_channel(913270148943732796).fetch_m(935396756139696159)
            await msg.edit(content = m.content[12:])
            await m.add_reaction(emoji='✅')
        else:
            await m.reply(f'Sorry, you need to either be my developer or have *manage_server* permissions on the NWYT server to use this command.')
            
    if m.channel.id == 937814975525842994:
        if not m.author.bot:
            try:
                pc = int(open('nwytcount','r').read())
                if int(m.content) == pc + 1:
                    f=open('nwytcount','w')
                    f.write(m.content)
                    f.close()
                    async with aiohttp.ClientSession() as session:
                        webhook = Webhook.from_url(open('tokens/NWYTwebhook','r').read(), adapter=AsyncWebhookAdapter(session))
                        await webhook.send(content=pc+1, username = m.author.name, avatar_url = m.author.avatar_url)   
                    await m.delete()     
                else:
                    raise Exception
            except Exception as e:
                await m.delete()    

@client.event
async def on_member_join(after):
    dat = open('NWYTbl','r').read().split()
    for e in dat:
        if e.lower() in after.name.lower() and not after.guild_permissions.administrator:
            await after.edit(nick=after.name.lower().replace(e.lower(),'dummy'))
            print(f"Updated {after} display name from {after.name} to {after.name.lower().replace(e.lower(),'dummy')}")
        if e.lower() in after.display_name.lower() and not after.guild_permissions.administrator:
            await after.edit(nick="")
            print(f"Updated {after} display name from {after.display_name} to {after.display_name.lower().replace(e.lower(),'dummy')}")       

client.run(open('tokens/nwyt','r').read())
