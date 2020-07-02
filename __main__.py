import discord, requests, json, re
from discord.ext.commands import Bot

BOT_PREFIX = (',')

with open("bot.txt") as f:
    ID, TOKEN = f.read().split(" ")

client = Bot(command_prefix=BOT_PREFIX)

headers = {"User-Agent": "Mozilla/5.0"}

max_dps_stats = {
    "Rogue": [50, 75],
    "Archer": [75, 50],
    "Wizard": [75, 75],
    "Priest": [50, 55],
    "Warrior": [75, 50],
    "Knight": [50, 50],
    "Paladin": [50, 45],
    "Assassin": [60, 75],
    "Necromancer": [75, 60],
    "Huntress": [75, 50],
    "Mystic": [60, 55],
    "Trickster": [65, 75],
    "Sorcerer": [70, 60],
    "Ninja": [70, 70],
    "Samurai": [75, 50],
    "Bard": [55, 70]
}
sbe = {
    "swords" : ["", "short-sword", "broad-sword", "saber", "long-sword", "falchion", "fire-sword", "glass-sword", "golden-sword", "ravenheart-sword", "dragonsoul-sword"],
    "daggers" : ["", "steel-dagger", "dirk", "blue-steel-dagger", "dusky-rose-dagger", "silver-dagger", "golden-dagger", "obsidian-dagger", "mithril-dagger", "fire-dagger", "ragetalon-dagger"],
    "bows" : ["", "shortbow", "reinforced-bow", "crossbow", "greywood-bow", "ironwood-bow", "fire-bow", "double-bow", "heavy-crossbow", "golden-bow", "verdant-bow"],
    "staves" : ["", "energy-staff", "firebrand-staff", "comet-staff", "serpentine-staff", "meteor-staff", "slayer-stuff", "avenger-staff", "staff-of-destruction", "staff-of-horror", "staff-of-necrotic-arcana"],
    "wands" : ["", "fire-wand", "force-wand", "power-wand", "missile-wand", "eldritch-wand", "hell-s-fire-wand", "wand-of-dark-magic", "wand-of-arcane-flame", "wand-of-death", "wand-of-deep-sorcery"],
    "katanas" : ["", "rusty-katana", "kendo-stick", "plain-katana", "thunder-katana", "line-kutter-katana", "night-edge", "sky-edge", "buster-katana", "demon-edge", "jewel-eye-katana"],
    "heavy_armor" : ["", "iron-mail", "chainmail", "blue-steel-mail", "silver-chainmail", "golden-chainmail", "plate-mail", "mithril-chainmail", "dragonscale-armor"],
    "leather_armor" : ["", "wolfskin-armor", "leather-armor", "basilisk-hide-armor", "minotaur-hide-armor", "bearskin-armor", "chimera-hide-armor", "wyvern-skin-armor", "studded-leather-armor", "drake-hide-armor"],
    "robes" : ["", "robe-of-the-neophyte", "robe-of-the-acolyte", "robe-of-the-student", "robe-of-the-conjurer", "robe-of-the-adept", "robe-of-the-invoker", "robe-of-the-illiusionist", "robe-of-the-master"],
    "rings" : ["", "ring-of-minor-defense", "ring-of-defense", "ring-of-greater-defense", "ring-of-superior-defense",
    "ring-of-health", "ring-of-greater-health", "ring-of-superior-health",
    "ring-of-magic", "ring-of-greater-magic", "ring-of-superior-magic",
    "ring-of-attack", "ring-of-greater-attack", "ring-of-superior-attack",
    "ring-of-dexterity", "ring-of-greater-dexterity", "ring-of-superior-dexterity",
    "ring-of-speed", "ring-of-greater-speed", "ring-of-superior-speed",
    "ring-of-vitality", "ring-of-greater-vitality", "ring-of-superior-vitality",
    "ring-of-wisdom", "ring-of-greater-wisdom", "ring-of-superior-wisdom",]
}
stats = ["att", "dex"]
banned_equipment = {
    "Rogue": [sbe["daggers"], [], sbe["leather_armor"], sbe["rings"], stats],
    "Archer": [sbe["bows"], [], sbe["leather_armor"], sbe["rings"], stats],
    "Wizard": [sbe["staves"], [], sbe["robes"], sbe["rings"], stats],
    "Priest": [sbe["wands"], [], sbe["robes"], sbe["rings"], stats],
    "Warrior": [sbe["swords"], [], sbe["heavy_armor"], sbe["rings"], stats],
    "Knight": [sbe["swords"], [], sbe["heavy_armor"], sbe["rings"], stats],
    "Paladin": [sbe["swords"], [], sbe["heavy_armor"], sbe["rings"], stats],
    "Assassin": [sbe["daggers"], [], sbe["leather_armor"], sbe["rings"], stats],
    "Necromancer": [sbe["staves"], [], sbe["robes"], sbe["rings"], stats],
    "Huntress": [sbe["bows"], [], sbe["leather_armor"], sbe["rings"], stats],
    "Mystic": [sbe["staves"], [], sbe["robes"], sbe["rings"], stats],
    "Trickster": [sbe["daggers"], [], sbe["leather_armor"], sbe["rings"], stats],
    "Sorcerer": [sbe["wands"], [], sbe["robes"], sbe["rings"], stats],
    "Ninja": [sbe["katanas"], [], sbe["leather_armor"], sbe["rings"], stats],
    "Samurai": [sbe["katanas"], [], sbe["heavy_armor"], sbe["rings"], stats],
    "Bard": [sbe["bows"], [], sbe["robes"], sbe["rings"], stats],
}
forced_equipment = {
    "Rouge": [[0], [0], [0], [0], 0],
    "Archer": [[0], [0], [0], [0], 0],
    "Wizard": [[0], [0], [0], [0], 0],
    "Priest": [[0], [0], [0], [0], 0],
    "Warrior": [[0], [0], [0], [0], 0],
    "Knight": [[0], [0], [0], [0], 0],
    "Paladin": [[0], [0], [0], [0], 0],
    "Assassin": [[0], [0], [0], [0], 0],
    "Necromancer": [[0], [0], [0], [0], 0],
    "Huntress": [[0], [0], [0], [0], 0],
    "Mystic": [[0], [0], [0], [0], 0],
    "Trickster": [[0], [0], [0], [0], 0],
    "Sorcerer": [[0], [0], [0], [0], 0],
    "Ninja": [[0], [0], [0], [0], 0],
    "Samurai": [[0], [0], [0], [0], 0],
    "Bard": [[0], [0], [0], [0], 0],
}

#def botPerms(user):
    #if(user.)

def checkStats(guild, igns, reqs="0", users=None):
    with open("setup.json") as f:
        d = json.load(f)
    banned = d[str(guild)]["equipment"][reqs]
    invisible = []
    meets = []
    doesnt = []
    if (len(igns)!=0):
        for i in range(len(igns)):
            worked = False
            try:
                IGN = igns[i]
                url = "https://www.realmeye.com/player/" + IGN
                request = requests.get(url=url, headers=headers)
                text = request.text
                data = text.split("<tbody>")
                data = data[1].split("<tr>")
                data = data[1].split("<td>")
                class_ = data[3].split("</td>")
                class_ = class_[0]
                equipment = data[9].split("item-wrapper")
                weapon = equipment[1].split("/wiki/")
                if (len(weapon) == 1):
                    weapon = ""
                else:
                    weapon = weapon[1].split("\"")
                    weapon = weapon[0]
                ability = equipment[2].split("/wiki/")
                if (len(ability) == 1):
                    ability = ""
                else:
                    ability = ability[1].split("\"")
                    ability = ability[0]
                armor = equipment[3].split("/wiki/")
                if (len(armor) == 1):
                    armor = ""
                else:
                    armor = armor[1].split("\"")
                    armor = armor[0]
                ring = equipment[4].split("/wiki/")
                if (len(ring) == 1):
                    ring = ""
                else:
                    ring = ring[1].split("\"")
                    ring = ring[0]
                stats = data[10].split("data-stats=\"[")
                stats = stats[1].split("]")
                stats = stats[0].split(",")
                bonus = data[10].split("data-bonuses=\"[")
                bonus = bonus[1].split("]")
                bonus = bonus[0].split(",")
                worked = True
            except:
                invisible.append(IGN)
                pass

            done = False
            # Stats
            if (worked and not (int(stats[2])-int(bonus[2])==max_dps_stats[class_][0] and int(stats[7])-int(bonus[7])==max_dps_stats[class_][1])):
                done = True
                if users is None:
                    doesnt.append(IGN)
                else:
                    doesnt.append([users[i], IGN])
            # Equipment
            elif (worked and (weapon in banned_equipment[class_][0] or ability in banned_equipment[class_][1] or armor in banned_equipment[class_][2] or ring in banned_equipment[class_][3])):
                done = True
                if users is None:
                    doesnt.append(IGN)
                else:
                    doesnt.append([users[i], IGN])
            else:
                if users is None:
                    meets.append(IGN)
                else:
                    meets.append([users[i], IGN])
    return ([invisible, meets, doesnt])

@client.event
async def on_ready():
    print('Ready')

@client.event
async def on_message(message):
    key = message.content.replace("\n", " ").replace(",", " ").replace("  ", " ")
    key = re.sub(" +", " ", key).split(" ")
    if(key[0]!="nexal"):
        return

    # Logging
    print(message.author.display_name + " | \"" + message.content + "\"")

    with open("setup.json") as f:
        d = json.load(f)

    # Announcement
    if (len(key)>1 and key[1]=="announcement" and message.author.id==381673088216989742):
        print(message.author.id)
        a = " ".join(key[2:])
        for i in client.guilds:
            print(i.id)
            print("\n")
            if (str(i.id) in d):
                print(i.id)
                print(d[str(i.id)])
                for j in d[str(i.id)]["bot_cs"]:
                    print(i.get_channel(j).id)
                    await i.get_channel(j).send(">>> **ANNOUCENMENT**\n" + a)
        return
                

    # Help
    if(len(key)>1 and key[1]=="help" and message.channel.id in d[str(message.guild.id)]["bot_cs"]):
        await message.channel.send("These are the following commands. Ones with an * can only be used by nexal admins.\n\n \
            **parse <vc#> <list of IGNs separated by space, comma, or a newline>** \nThis command does the role of a security. Do /who in the dungeon in RotMG and put all the names in the list of IGNs to parse VC and reqs.\n \
> nexal parse 1 cylia tbenz inmenro pizzawitch youapollo\n\n \
            **parse <vc#>** \nThis command only parses for stats of people in the VC. This can be highly useful if you would rather do /who and manually check VC while the bot is parsing for stats as this will allow you to not have to type everyone's name into the bot command.\n \
> nexal parse 1\n\n \
            **setup** *\nThis command sets up the server\n \
> nexal setup\n\n \
            **admins (add/del/see) <ID (for add/del)>** *\n This command lets you add, delete or see nexal admins on this server.\n \
> nexal admin add 381673088216989742\n \
> nexal admin del 381673088216989742\n \
> nexal admin see\n\n \
            **vcs (add/del/see) <ID (for add/del)>** *\n This command lets you add, delete or see nexal voice channels on this server.\n \
> nexal vcs add 713844221530079277\n \
> nexal vcs del 713844221530079277\n \
> nexal vcs see\n\n \
            **bcs (add/del/see) <ID (for add/del)>** *\n This command lets you add, delete or see nexal bot channels on this server.\n \
> nexal vcs add 713844221324427290\n \
> nexal vcs del 713844221324427290\n \
> nexal vcs see\n ")
        return

    # Setup
    if(len(key)>1 and key[1]=="setup"):
        if (message.author.id != 381673088216989742):
            await message.channel.send("Only nexal may set up the nexal bot.")
        else:
            setup = {
                "equipment": {0: banned_equipment},
                "forced": {0: forced_equipment},
                "admins": [381673088216989742],
                "vcs": [0],
                "bot_cs": []
            }
            d[message.guild.id] = setup
            with open("setup.json", "w") as f:
                json.dump(d, f)
            await message.channel.send("Setup complete! Now add nexal admins, voice channels, and text channels for the bot commands!")
        return

    # Check It's Setup
    if (str(message.guild.id) not in d):
        await message.channel.send("The nexal bot has not been setup yet. Please set it up via nexal.")
        return

    # Check It's in BOT_CS
    if (message.author.id != 381673088216989742 and message.channel.id not in d[str(message.guild.id)]["bot_cs"]):
        return

    # Admins
    if (len(key)>1 and key[1]=="admin" and (message.author.id == 381673088216989742 or message.author.id in d[str(message.guild.id)]["admins"])):
        if (len(key)>2 and key[2]=="add"):
            new_ = key[3:]
            print(new_)
            for i in new_:
                d[str(message.guild.id)]["admins"].append(int(i))
            with open("setup.json", "w") as f:
                json.dump(d, f)
            await message.channel.send("Added " + str(len(new_)) + " new nexal admins!")
        elif (len(key)>2 and key[2]=="del"):
            del_ = key[3:]
            for i in del_:
                d[str(message.guild.id)]["admins"].remove(int(i))
            with open("setup.json", "w") as f:
                json.dump(d, f)
            await message.channel.send("Deleted " + str(len(del_)) + " nexal admins!")
        elif (len(key)>2 and key[2]=="see"):
            message_ = "The " + str(len(d[str(message.guild.id)]["admins"])) + " nexal admins are: "
            for i in d[str(message.guild.id)]["admins"]:
                message_ += message.guild.get_member(i).mention + " "
            await message.channel.send(message_)
        return

    # VCS
    if (len(key)>1 and key[1]=="vcs" and (message.author.id == 381673088216989742 or message.author.id in d[str(message.guild.id)]["admins"])):
        if (len(key)>2 and key[2]=="add"):
            new_ = key[3:]
            print(new_)
            for i in new_:
                d[str(message.guild.id)]["vcs"].append(int(i))
            with open("setup.json", "w") as f:
                json.dump(d, f)
            await message.channel.send("Added " + str(len(new_)) + " new nexal vcs!")
        elif (len(key)>2 and key[2]=="del"):
            if (len(key)>3):
                for i in range(int(key[3])):
                    d[str(message.guild.id)]["vcs"].pop()
                with open("setup.json", "w") as f:
                    json.dump(d, f)
                await message.channel.send("Deleted " + key[3] + " vcs!")
            else:
                d[str(message.guild.id)]["vcs"].pop()
                with open("setup.json", "w") as f:
                    json.dump(d, f)
                await message.channel.send("Deleted 1 vc!")
        elif (len(key)>2 and key[2]=="see"):
            message_ = "The " + str(len(d[str(message.guild.id)]["vcs"])-1) + " nexal vcs are: "
            for i in d[str(message.guild.id)]["vcs"]:
                if (i==0):
                    continue
                message_ += message.guild.get_channel(i).mention + " "
            await message.channel.send(message_)
        return

    # BOT_CS
    if (len(key)>1 and key[1]=="bcs" and (message.author.id == 381673088216989742 or message.author.id in d[str(message.guild.id)]["admins"])):
        if (len(key)>2 and key[2]=="add"):
            new_ = key[3:]
            print(new_)
            for i in new_:
                d[str(message.guild.id)]["bot_cs"].append(int(i))
            with open("setup.json", "w") as f:
                json.dump(d, f)
            await message.channel.send("Added " + str(len(new_)) + " new nexal bot channels!")
        elif (len(key)>2 and key[2]=="del"):
            del_ = key[3:]
            for i in del_:
                d[str(message.guild.id)]["bot_cs"].remove(int(i))
            with open("setup.json", "w") as f:
                json.dump(d, f)
            await message.channel.send("Deleted " + str(len(del_)) + " nexal bot channel!")
        elif (len(key)>2 and key[2]=="see"):
            message_ = "The " + str(len(d[str(message.guild.id)]["bot_cs"])) + " nexal bot channels are: "
            for i in d[str(message.guild.id)]["bot_cs"]:
                message_ += message.guild.get_channel(i).mention + " "
            await message.channel.send(message_)
        return

    # Parse
    if(len(key)>1 and key[1]=="parse"):
        # VC Number + Reqs
        if(len(key)>2):
            reqs = "0"
            if (key[2][0] == "-"):
                reqs = key[2][1:]
            channel_number = 0
            try:
                channel_number = int(key[2])
            except:
                pass
            if(channel_number==0):
                return
        else:
            return

        # People in Dungeon
        if ((len(key)>3 and key[2][0] != "-") or len(key)>4):
            raiders = key[3:]
        else:
            raiders = []

        # People in VC
        vc_people = message.guild.get_channel(d[str(message.guild.id)]["vcs"][channel_number]).members

        crashers = []
        non_crashers = []

        not_in_server = []
        server_crashers = []

        invisible = []

        if ((len(key)>3 and key[2][0] != "-") or len(key)>4):
            # Check Crashers
            staffs = []
            for i in raiders:
                crashing = True
                id = 0
                for j in vc_people:
                    staff = False
                    discord_name = j.display_name.lower()
                    if (discord_name[0].lower() not in 'qwertyuiopasdfghjklzxcvbnm'):
                        staff = True
                    alts = discord_name.split(" | ")
                    if (staff):
                        alts[0] = alts[0][1:]
                    if (i.lower() in alts):
                        crashing = False
                        id = j.id
                        break
                if (crashing):
                    crashers.append(i)
                else:
                    non_crashers.append([id, i.lower()])

            # Check if Crasher is in Server
            for i in crashers:
                in_server = False
                id = 0
                for j in message.guild.members:
                    staff = False
                    discord_name = j.display_name.lower()
                    if (discord_name[0].lower() not in 'qwertyuiopasdfghjklzxcvbnm'):
                        staff = True
                    alts = discord_name.split(" | ")
                    if (staff):
                        alts[0] = alts[0][1:]
                    if (i.lower() in alts):
                        in_server = True
                        id = j.id
                        break
                if (in_server):
                    server_crashers.append([id, i.lower()])
                else:
                    not_in_server.append(i)

            # Check if Raiders Meet Reqs.
            temp1 = []
            temp2 = []
            for i in server_crashers:
                temp1.append(i[0])
                temp2.append(i[1])
            temp3, only_crashing, crashing_without_reqs = checkStats(message.guild.id, temp2, reqs, temp1)
            for i in temp3:
                invisible.append(i)

            temp1 = []
            temp2 = []
            for i in non_crashers:
                temp1.append(i[0])
                temp2.append(i[1])
            temp3, temp4, only_noreqs = checkStats(message.guild.id, temp2, reqs, temp1)
            for i in temp3:
                invisible.append(i)

            temp3, only_not_in_server, not_in_server_reqs = checkStats(message.guild.id, not_in_server, reqs)
            for i in temp3:
                invisible.append(i)
        else:
            IGNS = []
            for i in vc_people:
                if (i.display_name.lower()[0] not in 'qwertyuiopasdfghjklzxcvbnm'):
                    j = i.display_name[1:]
                else:
                    j = i.display_name
                
                alts = j.lower().split(" | ")
                for k in alts:
                    IGNS.append(k)
                    raiders.append(i.id)

            invisible, temp, only_noreqs = checkStats(message.guild.id, IGNS, reqs, raiders)
            only_crashing, crashing_without_reqs, only_not_in_server, not_in_server_reqs = [[], [], [], []]

            await message.channel.send("Beware for parses on alts not in the run. These are denoted with (alt).")

        # Send Message
        send_message = ">>> "
        if (len(invisible)!=0):
            send_message += "Invisible Realmeyes: "
            for i in invisible:
                send_message += i + " "
            send_message += "\n"
        if (len(only_not_in_server)!=0):
            send_message += "Not-In-Server Crashers: "
            for i in only_not_in_server:
                send_message += i + " "
            send_message += "\n"
        if (len(not_in_server_reqs)!=0):
            send_message += "Not-In-Server Crashers without Reqs: "
            for i in not_in_server_reqs:
                send_message += i + " "
            send_message += "\n"
        if (len(only_crashing)!=0):
            send_message += "Crashers: "
            for i in only_crashing:
                name = message.guild.get_member(i[0])
                if (name.display_name.lower() == i[1] or name.display_name[0] not in "qwertyuiopasdfghjklzxcvbnm"):
                    send_message += message.guild.get_member(i[0]).mention + " "
                else:
                    send_message += message.guild.get_member(i[0]).mention + " (" + i[1] + ") "
            send_message += "\n"
        if (len(only_noreqs)!=0):
            send_message += "Not Reqs: "
            for i in only_noreqs:
                name = message.guild.get_member(i[0])
                if (name.display_name.lower() == i[1] or name.display_name[0] not in "qwertyuiopasdfghjklzxcvbnm"):
                    send_message += message.guild.get_member(i[0]).mention + " "
                else:
                    send_message += message.guild.get_member(i[0]).mention + " (" + i[1] + ") "
            send_message += "\n"
        if (len(crashing_without_reqs)!=0):
            send_message += "Crashing without Reqs: "
            for i in crashing_without_reqs:
                name = message.guild.get_member(i[0])
                if (name.display_name.lower() == i[1] or name.display_name[0] not in "qwertyuiopasdfghjklzxcvbnm"):
                    send_message += message.guild.get_member(i[0]).mention + " "
                else:
                    send_message += message.guild.get_member(i[0]).mention + " (" + i[1] + ") "
            send_message += "\n"
        if(send_message==">>> "):
            send_message += "All Good!"
        await message.channel.send("Parse by " + message.author.mention + " is over.\n" + send_message)


client.run(TOKEN)