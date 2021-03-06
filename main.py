
import discord
import pymysql.cursors
from msqlsettings import *
import random
import asyncio
import aiohttp
import json
from discord import Game
from discord.ext.commands import Bot
from discord.ext import tasks
from discord.ext import commands

from settings import BOT_TOKEN


BOT_PREFIX = ("?", "!")
itemdict = {":socks: sock": 1,
            ":package: treasure box": 500,
            ":cheese: cheese": 5,
            ":shaved_ice: greek yogurt": 5,
            ":mans_shoe: shoe": 50,
            ":lab_coat: invisibility cloak": 50000,
            ":fire: flamethrower": 5000,
            ":tophat: hat": 50,
            ":fork_and_knife: fork": 1,
            "<:fishingpole:744360748628705351> fishing pole": 10000,
            "<:fish2:744379628377997312> fish": 100,
            "<:sword:746899181377028166> sword": 1000}

shopdict = {"<:sock:742981097947660289> `sock`": 1,
            "<:chese:742980033928364043> `cheese`": 10,
            "<:greekyogurt:742981685078917121> `greek yogurt`": 10,
            ":mans_shoe: `shoe`": 100,
            "<:invcloak:742551080117862521> `invisibility cloak`": 100000,
            "<:Flamethrower:742551466514055229> `flamethrower`": 10000,
            "<:Hat:742573525847506965> `hat`": 100,
            "<:fork:742983003625750539> `fork`": 5,
            "<:fishingpole:744360748628705351> `fishing pole`": 10000,
            "<:sword:746899181377028166> `sword`": 1000}

itemreduce = {"sock": 1,
              "treasurebox": 500,
              "cheese": 5,
              "greekyogurt": 5,
              "shoe": 50,
              "invisibilitycloak": 50000,
              "flamethrower": 5000,
              "hat": 50,
              "fork": 1,
              "fishingpole": 10000,
              "fish": 100,
              "sword": 1000}

shopreduce = {"sock": 1,
              "cheese": 10,
              "greekyogurt": 10,
              "shoe": 100,
              "invisibilitycloak": 100000,
              "flamethrower": 10000,
              "hat": 100,
              "fork": 5,
              "fishingpole": 10000,
              "sword": 1000}

questlist = {"1 Win a !hangman game.": 1000, "2 Get your pet to level 10.": 10000,
             "3 Use a flamethrower from the !shop": 1000,
             "4 Rob someone.": 1000, "5 Fight someone.": 1000, "6 Get to 100,000 coins.": 100000,
             "7 Get to a million coins.": 1000000}

creatures = ["fairy", "human", "elf", "robot", "cyborg", "demon", "werewolf", "vampire", "potato"]

occupationsdisp = ["<:wiz_hat:743635771264729119> `wizard`", "<:witchhat:743619195044102214> `witch`",
                   ":paintbrush: `artist`",
                   "<:ninja:743620991258722345> `ninja`", ":surfer: `surfer`", ":crown: `dictator`"]

occupations = ["wizard", "witch", "artist",
               "ninja", "surfer", "dictator"]

petlist = ["frog", "dog", "cat", "horse", "hamster", "dragon",
           "wolf", "snake", "crab", "bunny", "turtle", "tiger"]

petdisp = [":frog: `frog` ", ":dog2: `dog` ", ":cat: `cat` ", ":racehorse: `horse` ", ":hamster: `hamster` ",
           ":dragon: `dragon` ", ":wolf: `wolf` ", ":snake: `snake` ", ":crab: `crab` ", ":rabbit2: `bunny` ",
           ":turtle: `turtle`", ":tiger2: `tiger`"]


def connect_to():
    connection = pymysql.connect(host=DB_HOST,
                                 user=DB_USER,
                                 password=DB_PASS,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    print("{✧} Connected to database " + DB_NAME)
    return connection


class RPGLion:

    def __init__(self, token):
        self.db = connect_to()
        self.bot = Bot(command_prefix=BOT_PREFIX)
        self.token = token
        self.bot.remove_command('help')
        self.prepare()

    def add_u_db(self, member):
        exp = 0
        coin = 100
        inv = "treasurebox 1"
        clan = "none"
        lvl = 0
        creature = "human"
        occupation = "unemployed"
        pets = "none"
        isdonator = "no"
        quest = "none"
        if self.get_player(member):
            return

        try:
            with self.db.cursor() as cursor:
                sql = "INSERT INTO `players` (`user_id`, `first_seen`, `xp`, `coin`, `inv`, `clan`, `lvl`, `creature`,\
                 `occupation`, `pets`, `isdonator`, `quest`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) "
                cursor.execute(sql, (member.id, member.joined_at, exp, coin, inv,
                                     clan, lvl, creature, occupation, pets, isdonator, quest))
            self.db.commit()
            print("{✧} added " + str(member.id) + " to the database")
            # with connection.cursor() as cursor:
            #     # Read a single record
            #     sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
            #     cursor.execute(sql, ('webmaster@python.org',))
            #     result = cursor.fetchone()
            #     print(result)
        except Exception as e:
            print("{✧} error adding user: %s" % e)

    def run(self):
        self.bot.run(self.token)

    def prepare(self):

        @self.bot.command(name="help", description="shows commands", aliases=["Help", "commands", "Commands"],
                          pass_context=True)
        async def help(ctx, *, commandname=None):
            if commandname is None:
                helptext = ""
                for command in self.bot.commands:
                    helptext += f"`{command}` "
                embed = discord.Embed(
                    title="",
                    colour=discord.Colour.blurple(),
                    # url="https://discord.com/"
                )

                embed.add_field(
                    name="This is the list of commands. Type !help [command] to get more details about a command.",
                    value=helptext,
                    inline=False
                )

                embed.add_field(
                    name="donations",
                    value="[Donators get to be a dictator and have special privileges.]("
                          "https://www.patreon.com/join/5133324/checkout)",
                    inline=False
                )

                return await ctx.send(
                    content="",
                    embed=embed
                )
            else:
                helptext = ""
                for command in self.bot.commands:
                    helptext += f"{command}"
                if commandname not in helptext:
                    return await ctx.send("That command doesn't exist!")
                else:
                    for command in self.bot.commands:
                        if commandname == command.name:
                            alis = ""
                            for y in command.aliases:
                                alis += (y + " ")
                            embed = discord.Embed(
                                title="`" + command.name + "`",
                                colour=discord.Colour.blurple(),
                                # url="https://discord.com/"
                            )

                            embed.add_field(
                                name="description",
                                value=command.description,
                                inline=True
                            )

                            embed.add_field(
                                name="aliases",
                                value=alis,
                                inline=True
                            )

                            embed.add_field(
                                name="usage",
                                value=command.brief,
                                inline=True
                            )

                            embed.add_field(
                                name="donations",
                                value="[Donators get to be a dictator and have special privileges.]("
                                      "https://www.patreon.com/join/5133324/checkout)",
                                inline=False
                            )

                            return await ctx.send(
                                content="",
                                embed=embed
                            )
                    return "Uh oh! That command doesn't exist!"

        @self.bot.command(name="donate", description="donate info/donate/register as a donator",
                          brief="!donate", aliases=["Donate", "donations", "Donations"],
                          pass_context=True)
        async def donate(ctx):
            def check(ms):
                return ms.channel == ctx.message.channel and ms.author == ctx.message.author

            await ctx.send("Would you like to register as a donator? (y or n) \n"
                           "Donate at https://www.patreon.com/rpgLion .")
            donated = await self.bot.wait_for('message', check=check)
            if donated.content.lower() == 'y':
                await ctx.send("Please enter your discord tag:")
                disc_tag = await self.bot.wait_for('message', check=check, timeout=10)
                if not disc_tag:
                    return
                await ctx.send("Thanks! Please enter your Patreon username:")
                patreon_user = await self.bot.wait_for('message', check=check)
                bot_author = self.bot.get_user(471876600359813130)
                await bot_author.create_dm()
                await bot_author.dm_channel.send("Discord: " + disc_tag.content + "\n" + "Patreon: " +
                                                 patreon_user.content)
                return await ctx.send("Thank you for supporting us! It is very much appreciated. "
                                      "A message has been sent to us, and we will give you your perks as soon"
                                      "as we recieve your message and verify your donation. Thanks again!")
            else:
                return await ctx.send("No prob! Feel free to use this command again "
                                      "if you decide to register as a donator.")

        @self.bot.command(name="fight", description="fight someone", brief="!fight", aliases=["Fight", "duel", "Duel"],
                          pass_context=True)
        @commands.cooldown(1, 3600, commands.BucketType.user)
        async def fight(ctx, *, tofight: discord.Member = None):
            def check(ms):
                return ms.channel == ctx.message.channel and ms.author == ctx.message.author

            if self.get_q(ctx.author)['quest'] == "5 Fight someone.":
                self.update_q(ctx.author, "none")
                self.update_coin(ctx.author, questlist["5 Fight someone."])
                await ctx.send("Quest complete! You've been awarded " +
                               str(questlist["5 Fight someone."]) + " coins!")

            if not tofight:
                await ctx.send("Who do you want to fight?")
                tof = await self.bot.wait_for('message', check=check)
                tofight = tof.mentions[0]

            def check2(ms):
                return ms.channel == ctx.message.channel and ms.author == tofight

            await ctx.send(tofight.mention + ", do you accept the challenge? (expires in 5 seconds)")
            reponse = await self.bot.wait_for('message', check=check2)
            response2 = reponse.content
            if response2.lower() == "yes":
                score1 = 0
                score2 = 0
                def1 = 0
                def2 = 0
                for y in range(5):
                    await ctx.send(ctx.author.mention + ", what do you choose? \na) defend \nb) attack")
                    choice = await self.bot.wait_for('message', check=check)
                    if choice.content.lower() == "defend" or choice.content.lower() == "a":
                        def1 += 10
                        await ctx.send("You increase your defense")
                    elif choice.content.lower() == "attack" or choice.content.lower() == "b":
                        resultnum = random.randrange(101)
                        if resultnum > def1:
                            score1 += 10
                            await ctx.send("You attacked " + tofight.mention)
                        else:
                            await ctx.send("You missed!")
                    await ctx.send(tofight.mention + ", what do you choose? \na) defend \nb) attack")
                    choice2 = await self.bot.wait_for('message', check=check2)
                    if choice2.content.lower() == "defend" or choice2.content.lower() == "a":
                        def2 += 10
                        await ctx.send("You increase your defense")
                    elif choice2.content.lower() == "attack" or choice2.content.lower() == "b":
                        resultnum = random.randrange(101)
                        if resultnum > def2:
                            score2 += 10
                            await ctx.send("You attacked " + ctx.author.mention)
                        else:
                            await ctx.send("You missed!")
                    print(score1)
                    print(score2)
                if score1 > score2:
                    self.update_coin(ctx.author, 100)
                    self.update_coin(tofight, -100)
                    return await ctx.send(ctx.author.mention + " has defeated " + tofight.mention +
                                          " and has been awarded 100 of " + tofight.mention + "\'s coins!")
                if score2 > score1:
                    self.update_coin(ctx.author, -100)
                    self.update_coin(tofight, 100)
                    return await ctx.send(tofight.mention + " has defeated " + ctx.author.mention +
                                          " and has been awarded 100 of " + ctx.author.mention + "\'s coins!")
                else:
                    return await ctx.send("It's a tie!")
            else:
                return await ctx.send("They don't want to fight dude. Let them live in peace.")

        @self.bot.command(name="fish", description="go fishing", brief="!fish", aliases=["Fish"],
                          pass_context=True)
        @commands.cooldown(1, 10, commands.BucketType.user)
        async def fish(ctx):
            if "fishingpole" not in self.get_inv(ctx.author):
                return await ctx.send("You have to !buy a fishing pole from the !shop to fish.")
            outcomes = ["You caught nothing!", "You caught 1 fish!", "You caught 2 fish!"]
            out = random.choice(outcomes)
            if out == outcomes[0]:
                return await ctx.send(out)
            elif out == outcomes[1]:
                self.update_inv(ctx.author, "fish", 1)
                return await ctx.send(out)
            else:
                self.update_inv(ctx.author, "fish", 2)
                return await ctx.send(out)

        @self.bot.command(name="dice", description="roll a dice", brief="!dice", aliases=["Dice"],
                          pass_context=True)
        @commands.cooldown(1, 1, commands.BucketType.user)
        async def dice(ctx):
            outcomes = [1, 2, 3, 4, 5, 6]

            randoutcome = random.choice(outcomes)
            return await ctx.send("You rolled a " + str(randoutcome))

        @self.bot.command(name="_random", description="random event", brief="!random", aliases=["random", "Random"],
                          pass_context=True)
        @commands.cooldown(1, 86400, commands.BucketType.user)
        async def _random(ctx):
            randomlist = ["You found 100 coins!", "You found a treasure box!", "A ninja stole 100 coins from you!",
                          "You got attacked by a wild Karen!"]

            randevent = random.choice(randomlist)

            if randevent == randomlist[0]:
                self.update_coin(ctx.author, 100)
            if randevent == randomlist[1]:
                self.update_inv(ctx.author, "treasurebox", 1)
            if randevent == randomlist[2]:
                self.update_coin(ctx.author, -100)

            return await ctx.send(randevent)

        @self.bot.command(name="showquest", description="shows the quest you are on", brief="!showquest", aliases=["questlist"],
                          pass_context=True)
        @commands.cooldown(1, 3, commands.BucketType.user)
        async def showquest(ctx):
            return await ctx.send(self.get_q(ctx.author))

        @self.bot.command(name="quest", description="go on a quest", brief="!quest", aliases=["Quest"],
                          pass_context=True)
        @commands.cooldown(1, 60, commands.BucketType.user)
        async def quest(ctx):
            disp = ""
            for dood in questlist:
                disp += dood + " - " + str(questlist[dood]) + " coin prize.\n"
            embed = discord.Embed(
                title="Quests",
                colour=discord.Colour.blurple(),
                # url="https://discord.com/"
            )

            embed.add_field(
                name="Type the number of the quest you'd like, or type none/quit to select none/exit the command.",
                value=str(disp),
                inline=False
            )

            embed.add_field(
                name="donations",
                value="[Donators get to be a dictator and have special privileges.]("
                      "https://www.patreon.com/join/5133324/checkout)",
                inline=False
            )

            await ctx.send(
                content="",
                embed=embed
            )

            def check(ms):
                return ms.channel == ctx.message.channel and ms.author == ctx.message.author

            choicemsg = await self.bot.wait_for('message', check=check, timeout=20)
            qchoice = choicemsg.content
            if qchoice == "none" or qchoice == "quit":
                return await ctx.send("None selected")
            else:
                try:
                    value = int(qchoice)
                    if value > 7 or value < 1:
                        return await ctx.send("That is not a valid option.")
                    self.update_q(ctx.author, list(questlist)[value - 1])
                    return await ctx.send("You have selected the quest: " + list(questlist)[value - 1] + ". Good luck!")
                except ValueError:
                    return await ctx.send("That's not a number")

        @self.bot.command(name="hangman", description="cool game", brief="!hangman", aliases=["Hangman"],
                          pass_context=True)
        @commands.cooldown(1, 60, commands.BucketType.user)
        async def hangman(ctx):
            sticks = ["""Incorrect Guesses: 0\n
                            ------           
                            |       |           
                            |                  
                            |                  
                            |                  
                           -----            """,
                      """Incorrect Guesses: 1\n
                        ------           
                        |       |           
                        |      O           
                        |                  
                        |                  
                       -----            """,
                      """Incorrect Guesses: 2\n
                        ------          
                        |       |           
                        |      O           
                        |       |          
                        |                  
                       -----            """,
                      """Incorrect Guesses: 3\n
                        ------          
                        |       |           
                        |    \\O           
                        |       |           
                        |                  
                       -----            """,
                      """Incorrect Guesses: 4\n
                        ------          
                        |       |           
                        |    \\O/          
                        |       |           
                        |                  
                       -----            """,
                      """Incorrect Guesses: 5\n
                        ------          
                        |       |           
                        |    \\O/          
                        |       |           
                        |     /            
                       -----            """,
                      """Incorrect Guesses: 6\n
                        ------           
                        |       |           
                        |    \\O/          
                        |       |           
                        |     / \\           
                       -----            """
                      ]

            guesses = 0
            wrongs = 0
            correct = 0
            guessed = ""
            wordGs = []
            correctHint = ["h", "i", "n", "t", ":", " "]
            gameStatus = ""

            huge_list = []
            with open('words.txt', "r") as f:
                huge_list = f.read().split()

            guessW = ""

            def restartGame():
                global guessed
                global guesses
                global wrongs
                global correct
                global wordGs
                global gameStatus
                global correctHint
                guessed = ""
                guesses = 0
                wrongs = 0
                correct = 0
                wordGs = []
                gameStatus = ""
                correctHint = ["h", "i", "n", "t", ":", " "]

            def check(ms):
                return ms.channel == ctx.message.channel and ms.author == ctx.message.author

            if (gameStatus == ""):
                guessW = random.choice(huge_list)
                for char in guessW:
                    correctHint += "-"
                    correctHint += " "
                print(correctHint)
                correctH2 = ""
                for f in correctHint:
                    correctH2 += f
                phrase = sticks[0] + "\n" + correctH2 + "\nEnter a guess, no more than " + str(
                    len(guessW)) + " characters."
                await ctx.send(phrase)
                msg = await self.bot.wait_for('message', check=check)
                guesses += 1
                gues = msg.content
                if (gues.isupper()):
                    gues = gues.lower()
                count = 0
                if (len(gues) == 1):
                    count2 = 0
                    for x in guessW:
                        if (gues == x):
                            indd2 = 6 + (2 * count2)
                            correctHint[indd2] = x
                            count += 1
                        count2 += 1
                    print(guessW)
                    if (count < 1):
                        wrongs += 1
                        gameStatus = "playing"
                        guessed += gues
                        phrase = "No " + gues + "'s. Wrong: " + str(
                            wrongs) + ". Enter !hangman to continue entering guesses."
                        await ctx.send(phrase)
                    else:
                        correct += count
                        guessed += gues
                        gameStatus = "playing"
                        if (correct == len(guessW)):
                            phrase = sticks[wrongs] + "\nYou got it! The word is " + guessW
                            if self.get_q(ctx.author) == "1 Win a !hangman game.":
                                self.update_q(ctx.author, "none")
                            restartGame()
                            return await ctx.send(phrase)
                        phrase = str(count) + " " + gues + "'s! Wrong: " + str(wrongs) + ". Enter !hangman to continue."
                        await ctx.send(phrase)
                else:
                    if (len(gues) != len(guessW)):
                        gameStatus = "playing"
                        await ctx.send(
                            "Too many/too few characters. Guess again with " + str(len(guessW)) + " characters.")
                    else:
                        if (gues in wordGs):
                            wrongs += 1
                            await ctx.send("You already guessed that, type !hangman to guess something else")
                            if (wrongs == 6):
                                phrase = sticks[wrongs] + "\nOut of guesses! The word is " + guessW + ". Try again."
                                restartGame()
                                return await ctx.send(phrase)
                        else:
                            wordGs += gues
                            wordGs += " "
                            if (gues == guessW):
                                phrase = sticks[wrongs] + "\nYou got it! The word is " + guessW
                                restartGame()
                                return await ctx.send(phrase)
                            else:
                                wrongs += 1
                                guesses += 1
                                gameStatus = "playing"
                                phrase = "No " + gues + " is not the word. Wrong: " + str(
                                    wrongs) + ". Enter !hangman to continue entering guesses."
                                await ctx.send(phrase)
            while (gameStatus != ""):
                gcdisplay = ""
                for r in guessed:
                    gcdisplay += (r + ", ")
                gwdisplay = ""
                for u in wordGs:
                    if (u == " "):
                        u = ", "
                    gwdisplay += u
                correctH2 = ""
                for f in correctHint:
                    correctH2 += f
                phrase = sticks[wrongs] + "\n" + correctH2 + "\nEnter a guess, no more than " + str(
                    len(guessW)) + " characters."
                phrase2 = phrase + "\nLetters guessed: " + gcdisplay + ". Words guessed: " + gwdisplay + "."
                await ctx.send(phrase2)
                msg = await self.bot.wait_for('message', check=check)
                guesses += 1
                gues = msg.content
                if (gues.isupper()):
                    gues = gues.lower()
                if (len(gues) == 1):
                    if gues in guessed:
                        wrongs += 1
                        await ctx.send("You already guessed that.")
                        if (wrongs == 6):
                            phrase = sticks[wrongs] + "\nOut of guesses! The word is " + guessW + ". Try again."
                            restartGame()
                            return await ctx.send(phrase)
                    else:
                        count2 = 0
                        count = 0
                        for x in guessW:
                            if (gues == x):
                                indd2 = 6 + (2 * count2)
                                correctHint[indd2] = x
                                count += 1
                            count2 += 1
                        print(guessW)
                        print(count)
                        if (count < 1):
                            wrongs += 1
                            guessed += gues
                            if (wrongs == 6):
                                phrase = sticks[wrongs] + "\nOut of guesses! The word is " + guessW + ". Try again."
                                restartGame()
                                return await ctx.send(phrase)
                            gameStatus = "playing"
                            phrase = "No " + gues + "'s. Wrong: " + str(
                                wrongs) + ". Enter !hangman to continue entering guesses."
                            await ctx.send(phrase)
                        else:
                            correct += count
                            guessed += gues
                            gameStatus = "playing"
                            print(correct)
                            if (correct == len(guessW)):
                                phrase = sticks[wrongs] + "\nYou got it! The word is " + guessW
                                restartGame()
                                return await ctx.send(phrase)
                            phrase = str(count) + " " + gues + "'s! Wrong: " + str(
                                wrongs) + ". Enter !hangman to continue."
                            await ctx.send(phrase)
                else:
                    print(guessW)
                    if (len(gues) != len(guessW)):
                        gameStatus = "playing"
                        await ctx.send(
                            "Too many/too few characters. Guess again with " + str(len(guessW)) + " characters.")
                    else:
                        isUsed = False
                        placehold = ""
                        for wo in wordGs:
                            if (wo != " "):
                                placehold += wo
                            if (wo == " "):
                                if (placehold == gues):
                                    isUsed = True
                                placehold = ""
                        if (isUsed):
                            wrongs += 1
                            await ctx.send("You already guessed that.")
                            if (wrongs == 6):
                                phrase = sticks[wrongs] + "\nOut of guesses! The word is " + guessW + ". Try again."
                                restartGame()
                                return await ctx.send(phrase)
                        else:
                            wordGs += gues
                            wordGs += " "
                            if (gues == guessW):
                                phrase = sticks[wrongs] + "\nYou got it! The word is " + guessW
                                restartGame()
                                return await ctx.send(phrase)
                            else:
                                wrongs += 1
                                guesses += 1
                                if (wrongs == 6):
                                    phrase = sticks[wrongs] + "\nOut of guesses! The word is " + guessW + ". Try again."
                                    restartGame()
                                    return await ctx.send(phrase)
                                gameStatus = "playing"
                                phrase = "No '" + gues + "' is not the word. Wrong: " + str(
                                    wrongs) + ". Enter !hangman to continue entering guesses."
                                await ctx.send(phrase)

        @self.bot.command(name="daily", description="daily coins", brief="!daily", aliases=["Daily"],
                          pass_context=True)
        @commands.cooldown(1, 86400, commands.BucketType.user)
        async def daily(ctx):
            self.update_coin(ctx.author, 100)
            return await ctx.send("You got 100 coins. Come back again tomorrow for more.")

        @self.bot.command(name="pat", description="pat your pets (which increases their xp)", brief="!pat",
                          aliases=["Pat"],
                          pass_context=True)
        @commands.cooldown(1, 10, commands.BucketType.user)
        async def pat(ctx):
            if len(self.get_pets(ctx.author)) < 1 or (list(self.get_pets(ctx.author)))[0] == "none":
                return await ctx.send("You don't have any pets to pat! :(")
            for x in self.get_pets(ctx.author):
                self.update_pet_xp(ctx.author, self.get_pets(ctx.author)[x], x, 1)
            return await ctx.send("You pat all your pets.")

        @self.bot.command(name="pet", description="get a pet", brief="!pet", aliases=["Pet"],
                          pass_context=True)
        @commands.cooldown(1, 60, commands.BucketType.user)
        async def pet(ctx):
            await ctx.send("Select your pet")
            disp = ""
            for dood in petdisp:
                disp += dood + "\n"
            embed = discord.Embed(
                title="Pets",
                colour=discord.Colour.blurple(),
                # url="https://discord.com/"
            )

            embed.add_field(
                name="Who's going home with you today?",
                value=str(disp),
                inline=False
            )

            embed.add_field(
                name="donations",
                value="[Donators get to be a dictator and have special privileges.]("
                      "https://www.patreon.com/join/5133324/checkout)",
                inline=False
            )

            await ctx.send(
                content="",
                embed=embed
            )

            def check(ms):
                return ms.channel == ctx.message.channel and ms.author == ctx.message.author

            pet = await self.bot.wait_for('message', check=check)
            pet2 = self.sanitize_item(pet.content)
            if pet2 not in petlist:
                return await ctx.send("That pet doesn't exist!")
            await ctx.send("What would you like to name your new pet?")
            pname = await self.bot.wait_for('message', check=check)
            pname2 = pname.content
            if list(self.get_pets(ctx.author))[0] != "none" and not self.is_donator(ctx.author):
                await ctx.send("It looks like you already have a " + self.disp_pets(ctx.author) +
                               ". Would you like to add this pet or replace the one you have? "
                               "Type a to add or r to replace")
                answerchoice = await self.bot.wait_for('message', check=check)
                answer = answerchoice.content
                if answer.lower() == 'r':
                    self.replace_pet(ctx.author, list(self.get_pets(ctx.author))[0],
                                     self.get_pets(ctx.author)[list(self.get_pets(ctx.author))[0]], pet2, pname2)
                    return await ctx.send("You replaced your old pet with a new " + pet2 + " named " + pname2)
                else:
                    if self.is_donator(ctx.author):
                        if pet2 in self.get_pets(ctx.author) and pname2 in self.get_pets(ctx.author)[pet2]:
                            return await ctx.send("Sorry, you can't have multiple " + pet2 + "s named " + pname2 +
                                                  ". Select another pet or name.")
                        self.update_pets(ctx.author, pet2, pname2, "add")
                        return await ctx.send("Added new pet " + pet2 + " named " + pname2 + " to your pets.")
                    await ctx.send("Donators get to have more than one pet. https://www.patreon.com/rpgLion")
                    await ctx.send("It looks like you already have a " + self.disp_pets(ctx.author) +
                                   ". Would you like to add this pet or replace the one you have? "
                                   "Type a to add or r to replace")
                    answerchoice2 = await self.bot.wait_for('message', check=check)
                    answer2 = answerchoice2.content
                    if answer2.lower() == 'r':
                        self.replace_pet(ctx.author, list(self.get_pets(ctx.author))[0],
                                         self.get_pets(ctx.author)[list(self.get_pets(ctx.author))[0]], pet2, pname2)
                        return await ctx.send("You replaced your old pet with a new " + pet2 + " named " + pname2)
                    else:
                        return await ctx.send("Sorry, only donators can have more than one pet.")
            if pet2 in self.get_pets(ctx.author) and pname2 in self.get_pets(ctx.author)[pet2]:
                return await ctx.send("Sorry, you can't have multiple " + pet2 + "s named " + pname2 +
                                      ". Select another pet or name.")
            self.update_pets(ctx.author, pet2, pname2, "add")

            return await ctx.send("You now have a new pet "
                                  + pet2 + " named " + pname2 +
                                  ". Type !pat to pat your pet, and type !profile or !mypets to see your pets.")

        @self.bot.command(name="abandonpet", description="to let your pet go", brief="!abandonpet", aliases=["abandon"],
                          pass_context=True)
        async def abandonpet(ctx):
            def check(ms):
                return ms.channel == ctx.message.channel and ms.author == ctx.message.author

            await ctx.send("What pet do you want to abandon? (name)")
            petname = await self.bot.wait_for('message', check=check)
            await ctx.send("Okay, what kind of pet is " + petname.content + "? (species)")
            petspecies = await self.bot.wait_for('message', check=check)
            petsp = petspecies.content.lower()
            if petsp not in self.get_pets(ctx.author) or petname.content \
                    not in self.get_pets(ctx.author)[petspecies.content.lower()]:
                return await ctx.send("Oh, you don't have a "
                                      + petspecies.content.lower() + " named " + petname.content)
            self.update_pets(ctx.author, petsp, petname.content, "remove")
            return await ctx.send("You gave " + petname.content + " to the animal shelter.")

        @self.bot.command(name="prestige", description="resets everything for you", brief="!prestige",
                          aliases=["Prestige"],
                          pass_context=True)
        @commands.cooldown(1, 86400, commands.BucketType.user)
        async def prestige(ctx):
            await ctx.send("Are you sure? All your inventory, xp, and coins will be reset. Reply `yes` or `no`")

            def check(ms):
                return ms.channel == ctx.message.channel and ms.author == ctx.message.author

            response = await self.bot.wait_for('message', check=check)

            if response.content.lower() == "yes":
                self.update_coin(ctx.author, -(int(self.get_coin(ctx.author)['coin'])))
                self.update_xp(ctx.author, -(int(self.get_xp(ctx.author)['xp'])))
                self.update_occ(ctx.author, "unemployed")
                self.update_char(ctx.author, "human")
                self.update_clan(ctx.author, "none")
                self.update_inv(ctx.author, "clear", 1)
                self.clear_lvl(ctx.author)
                self.clear_pets(ctx.author)
                self.update_q(ctx.author, "none")
                return await ctx.send("Everything has been reset.")
            else:
                return await ctx.send("Cancelled")

        # @self.bot.command(pass_context=True)
        # async def debug(ctx, emoji: discord.Emoji):
        #     embed = discord.Embed(description=f"emoji: {emoji}", title=f"emoji: {emoji}")
        #     embed.add_field(name="id", value=repr(emoji.id))
        #     embed.add_field(name="name", value=repr(emoji.name))
        #     await ctx.send(embed=embed)

        @self.bot.command(name="work", description="Work in your occupation to earn coins, xp, and cool stuff.",
                          aliases=["Work"], brief="!work",
                          pass_context=True)
        @commands.cooldown(1, 86400, commands.BucketType.user)
        async def work(ctx):
            try:
                job = self.get_occ(ctx.author)['occupation']
                if job not in occupations:
                    return await ctx.send("Sorry, you don't have a job. Get an occupation by typing !jobs.")

                async def one():
                    words = ["behold", "blithe", "evanescent", "flaxen", "isle", "sans", "slumber", "summer"]
                    mess = False
                    for x in range(5):
                        randword = random.choice(words)
                        await ctx.send("Type the word as fast as you can to chant your spells: `" + randword + "`")

                        def check(ms):
                            return ms.channel == ctx.message.channel and ms.author == ctx.message.author

                        word = await self.bot.wait_for('message', check=check)
                        if word.content.lower() != randword:
                            mess = True
                            break
                    if mess:
                        return "Your spell went wonky. You caught fire and lost 100 coins."
                    else:
                        self.update_coin(ctx.author, 100)
                        self.update_xp(ctx.author, 100)
                        return "You materialised 100 coins and gained 100 xp."

                async def two():
                    ings = ["sand", "flowers", "water", "sugar", "honey", "egg", "roses", "chamomile", "lavender"]
                    inghint = ["-a-d", "f--we-s", "-at--", "s-g--", "-one-", "e--", "-o-e-", "c---om-le", "l-ve-d--"]
                    mess = False
                    for x in range(5):
                        randpos = random.randint(0, len(ings) - 1)
                        randhint = inghint[randpos]
                        randword = ings[randpos]
                        print(randhint + " " + randword)
                        await ctx.send("Guess the potion ingredient: `" + randhint + "`")

                        def check(ms):
                            return ms.channel == ctx.message.channel and ms.author == ctx.message.author

                        word = await self.bot.wait_for('message', check=check)
                        if word.content != randword:
                            mess = True
                            break
                    if mess:
                        return "Your potion exploded. You got your eyebrows burned off and lost 100 coins."
                    else:
                        self.update_coin(ctx.author, 100)
                        self.update_xp(ctx.author, 100)
                        return "Your potion turned into 100 coins and gained 100 xp."

                async def three():
                    dice = [1, 2, 3, 4, 5, 6]

                    option = dice[random.randint(0, len(dice) - 1)]

                    result = ""

                    if option == 1:
                        result = "Nobody wants to buy your painting."
                    elif option == 2:
                        self.update_coin(ctx.author, 10)
                        self.update_xp(ctx.author, 10)
                        result = "Your friend buys your painting for 10 coins, and you gain 10 xp."
                    elif option == 3:
                        self.update_coin(ctx.author, 50)
                        self.update_xp(ctx.author, 50)
                        result = "Someone buys your painting for 50 coins, and you gain 50 xp."
                    elif option == 4:
                        self.update_coin(ctx.author, 100)
                        self.update_xp(ctx.author, 100)
                        result = "A couple of people are interested in your art, and one buys it for 100 coins. " \
                                 "You gain 100 xp."
                    elif option == 5:
                        self.update_coin(ctx.author, 200)
                        self.update_xp(ctx.author, 200)
                        result = "Your art gets featured in a small gallery, and someone buys it for 200 coin. " \
                                 "You get 200 xp."
                    elif option == 6:
                        self.update_coin(ctx.author, 1000)
                        self.update_xp(ctx.author, 1000)
                        result = "You're a modern Picasso! Your painting is featured in a museum, " \
                                 "and the museum pays you 1000 dollars for it. You gain 1000 xp."

                    return result

                async def four():
                    def check(ms):
                        return ms.channel == ctx.message.channel and ms.author == ctx.message.author

                    mess = False
                    res = ""
                    for x in range(5):
                        await ctx.send("Type `stealth`")
                        msg = await self.bot.wait_for('message', check=check)
                        if msg.content != "stealth":
                            mess = True
                            break

                    if mess:
                        res = "You weren't stealthy enough and got caught!"
                    else:
                        await ctx.send("Do you want to steal from a random person or someone specific? "
                                       "Type `random` for a random person or a user for someone specific.")
                        choiceee = await self.bot.wait_for('message', check=check)
                        if choiceee.content.lower() == "random":
                            randuser = self.get_a_user()
                        else:
                            randuser = choiceee.mentions[0]
                        if randuser == ctx.author:
                            while randuser == ctx.author:
                                randuser = self.get_a_user()
                                if randuser != ctx.author:
                                    break
                        inv1 = self.get_inv(randuser)
                        if inv1 == {}:
                            return "The user your were trying to rob had nothing to steal!"
                        randitem = key, val = random.choice(list(inv1.items()))
                        randitem2 = randitem[0]
                        if randitem2 == "invisibilitycloak":
                            while randitem2 == "invisibilitycloak":
                                randitem = key, val = random.choice(list(inv1.items()))
                                randitem2 = randitem[0]
                        self.update_inv(randuser, randitem2, -1)
                        self.update_inv(ctx.author, randitem2, 1)

                        res = "Mission successful! You snuck around and stole stole " \
                              "1 " + randitem2 + " from user <@" + str(randuser.id) + "> while they weren't watching."
                    return res

                async def five():
                    reamsg = await ctx.send("Let's catch some gnarly waves, dude! "
                                            "When I say up, click the up arrow. Down, down arrow. "
                                            "Left, left, right right and so forth")

                    await reamsg.add_reaction('⬆')
                    await reamsg.add_reaction('➡')
                    await reamsg.add_reaction('⬇')
                    await reamsg.add_reaction('⬅')
                    await asyncio.sleep(5)

                    def check(reaction, user):
                        return user == ctx.author

                    randwords = ["up", "down", "left", "right"]
                    for z in range(5):
                        await reamsg.delete()
                        direc = random.choice(randwords)
                        reamsg = await ctx.send("`" + direc + "`")
                        await reamsg.add_reaction('⬆')
                        await reamsg.add_reaction('➡')
                        await reamsg.add_reaction('⬇')
                        await reamsg.add_reaction('⬅')
                        reac, user = await self.bot.wait_for('reaction_add', check=check)
                        checkreac = ''
                        if direc == "up":
                            checkreac = '⬆'
                        elif direc == "right":
                            checkreac = '➡'
                        elif direc == "down":
                            checkreac = '⬇'
                        elif direc == "left":
                            checkreac = '⬅'

                        if str(reac) != checkreac:
                            return "You ate it brah."

                    self.update_coin(ctx.author, 100)
                    self.update_xp(ctx.author, 100)
                    return "Cowabunga! You got 100 coin and 100 xp from winning the surfing competition. Totally rad."

                def get_Duties(argument):
                    switcher = {
                        "wizard": one,
                        "witch": two,
                        "artist": three,
                        "ninja": four,
                        "surfer": five
                    }
                    func = switcher.get(argument)
                    return func()

                phrase = await get_Duties(job)
                return await ctx.send(phrase)

            except Exception as e:
                return await ctx.send(str(e))

        @self.bot.command(name="buy", description="buy an item from shop",
                          aliases=["Buy", "purchase", "Purchase"], brief="!buy [quantity] [item]",
                          pass_context=True)
        @commands.cooldown(1, 5, commands.BucketType.user)
        async def buy(ctx, *args):
            item = ""
            try:
                for x in range(1, len(args)):
                    item += args[x]
                quantity = int(args[0])

                item2 = self.sanitize_item(item)
                if item2 not in shopreduce:
                    return await ctx.send("That item is not in the shop")
                if quantity > 1:
                    if (int(self.get_coin(ctx.author)['coin']) - quantity * shopreduce[item2]) <= 0:
                        return await ctx.send("You don't have enough coins for that.")
                    self.update_inv(ctx.author, item2, quantity)
                    self.update_coin(ctx.author, -quantity * shopreduce[item2])
                    return await ctx.send("You bought " + str(quantity) + " " + item + "\'s.")
                if (int(self.get_coin(ctx.author)['coin']) - quantity * shopreduce[item2]) <= 0:
                    return await ctx.send("You don't have enough coins for that.")
                self.update_inv(ctx.author, item2, 1)
                self.update_coin(ctx.author, -shopreduce[item2])
                return await ctx.send("You bought 1 " + item + ".")
            except Exception as e:
                print(e)
                return await ctx.send("The syntax for the buy command is !buy [quantity] [item]. Type !shop to see "
                                      "the list of items you can buy.")

        @self.bot.command(name="balance", description="show your balance", brief="!balance *optional - [user]*)",
                          aliases=["coin balance", "Balance", "bal",
                                   "Bal"],
                          pass_context=True)
        @commands.cooldown(1, 5, commands.BucketType.user)
        async def balance(ctx, *, member: discord.Member = None):
            if not member:
                member = ctx.message.author
            coinbal = int(self.get_coin(member)['coin'])

            embed = discord.Embed(
                title=member.display_name + "\'s balance: `" + str(coinbal) + " coins`",
                colour=member.color,
                # url="https://discord.com/"
            )
            embed.set_thumbnail(url=member.avatar_url)
            embed.add_field(
                name="donations",
                value="[Donators get to be a dictator and have special privileges.]("
                      "https://www.patreon.com/join/5133324/checkout)",
                inline=False
            )

            await ctx.send(
                content="",
                embed=embed
            )

        @self.bot.command(name="shop", description="displays the shop with items to buy",
                          brief="!shop", aliases=["store", "Store", "Shop"],
                          pass_context=True)
        @commands.cooldown(1, 5, commands.BucketType.user)
        async def shop(ctx):
            disp = ""
            for item in shopdict:
                disp += "**" + item + "** - " + str(shopdict[item]) + " coins \n\n"
            embed = discord.Embed(
                title="",
                colour=discord.Colour.blurple(),
                # url="https://discord.com/"
            )

            embed.add_field(
                name="the shop",
                value=str(disp),
                inline=False
            )

            embed.add_field(
                name="donations",
                value="[Donators get to be a dictator and have special privileges.]("
                      "https://www.patreon.com/join/5133324/checkout)",
                inline=False
            )

            await ctx.send(
                content="",
                embed=embed
            )

        @self.bot.command(name="flamethrower", description="burn ppl", brief="!flamethrower",
                          aliases=["Flame", "flame", "Flamethrower"], pass_context=True)
        @commands.cooldown(1, 60, commands.BucketType.user)
        async def flamethrower(ctx):
            if self.get_q(ctx.author)['quest'] == "3 Use a flamethrower from the !shop":
                self.update_q(ctx.author, "none")
                self.update_coin(ctx.author, questlist["3 Use a flamethrower from the !shop"])
                await ctx.send("Quest complete! You've been awarded " +
                               str(questlist["3 Use a flamethrower from the !shop"]) + " coins!")
            if "flamethrower" not in self.get_inv(ctx.author):
                return await ctx.send("You don't have a flamethrower. !buy one from the !shop.")
            await ctx.send("Who do you want to burn?")

            def check(ms):
                return ms.channel == ctx.message.channel and ms.author == ctx.message.author

            toburn = await self.bot.wait_for('message', check=check)
            toburn2 = toburn.mentions[0]
            if int(self.get_coin(toburn2)['coin']) < 1 or int(self.get_coin(toburn2)['coin']) - 1000 < 1:
                return await ctx.send("You burnt " + toburn2.display_name + "\'s eyebrows off!")
            self.update_coin(toburn2, -1000)
            phrase2 = ""
            if "invisibilitycloak" in self.get_inv(toburn2):
                self.update_inv(toburn2, "invisibilitycloak", -1)
                phrase2 = "You also burned " + toburn.content + "\'s invisibility cloak! Ninjas can now steal " \
                                                                "their items!"

            return await ctx.send("The flamethrower burned up 1000 of " + toburn.content + "\'s coins." + phrase2)

        @self.bot.command(name="use", description="allows player to use their items for a variety of fun outcomes",
                          brief="!use [quantity] [item]", aliases=["Open", "Use", "open"],
                          pass_context=True)
        @commands.cooldown(1, 2, commands.BucketType.user)
        async def use(ctx, *args):
            item = ""
            try:
                for x in range(1, len(args)):
                    item += args[x]
                quantity = int(args[0])
                item2 = self.sanitize_item(item)
                if item2 not in self.get_inv(ctx.author):
                    return await ctx.send("You don't have a " + item)
                if int(self.get_inv(ctx.author)[item2]) < quantity:
                    return await ctx.send("You don't have " + str(quantity) + " " + item + "s.")
                if item2 == "treasurebox":
                    choicee = 0
                    for y in range(quantity):
                        await ctx.send("Opening treasure box...")
                        self.update_inv(ctx.author, "treasurebox", -1)
                        possible = [100, 200, 300, 400, 500, 100000]
                        choicee += random.choice(possible)
                    self.update_coin(ctx.author, choicee)
                    return await ctx.send("You used " + str(quantity) + " treasure box and gained " + str(choicee) +
                                          " coins. Niiice.")
                if item2 == "greekyogurt":
                    self.update_inv(ctx.author, item2, -quantity)
                    self.update_xp(ctx.author, (100 * quantity))
                    return await ctx.send(
                        "You ate " + str(quantity) + " greek yogurt and gained " + str(100 * quantity) + " xp.")
                if item2 == "invisibilitycloak":
                    return await ctx.send("This item is already active because it is in your inventory!")
            except Exception as e:
                return await ctx.send("The syntax for the use command is !use [quantity] [item].")

            self.update_inv(ctx.author, item2, -quantity)
            return await ctx.send("You used " + str(quantity) + " " + item + "s.")

        @self.bot.command(name="occupation", description="gets user a different occupation",
                          brief="!occupation", aliases=["Occupation", "job", "Job", "jobs", "Jobs"],
                          pass_context=True)
        @commands.cooldown(1, 86400, commands.BucketType.user)
        async def occupation(ctx):
            await ctx.send("Select your occupation")
            disp = ""
            for dood in occupationsdisp:
                disp += dood + "\n\n"
            embed = discord.Embed(
                title="Occupations",
                colour=discord.Colour.blurple(),
                # url="https://discord.com/"
            )

            embed.add_field(
                name="What would you like to be?",
                value=str(disp),
                inline=False
            )

            embed.add_field(
                name="donations",
                value="[Donators get to be a dictator and have special privileges.]("
                      "https://www.patreon.com/join/5133324/checkout)",
                inline=False
            )

            await ctx.send(
                content="",
                embed=embed
            )

            def check(ms):
                return ms.channel == ctx.message.channel and ms.author == ctx.message.author

            character = await self.bot.wait_for('message', check=check)
            character2 = self.sanitize_item(character.content)
            if character2 not in occupations:
                return await ctx.send("You can be anything within the list lol. Use the command again with a job from "
                                      "the list.")
            if character2 == "dictator":
                return await ctx.send("Donators"
                                      " get to be dictator which allows you to levy taxes on other players."
                                      "Donate link: https://www.patreon.com/join/5133324/checkout Otherwise, choose one"
                                      "of the other occupations.")
            self.update_occ(ctx.author, character2)

            return await ctx.send("Your occupation is now " + character.content + ". Type !work to work in your new "
                                                                                  "occupation.")

        @self.bot.command(name="creature", description="gets user a different creature",
                          brief="!creature", aliases=["char", "Char", "Character", "character", "Creature"],
                          pass_context=True)
        @commands.cooldown(1, 5, commands.BucketType.user)
        async def creature(ctx):
            await ctx.send("Select your creature")
            disp = ""
            for dood in creatures:
                disp += "**" + dood + "** - " + dood + "\n\n"
            embed = discord.Embed(
                title="You can be anything!",
                colour=discord.Colour.blurple(),
                # url="https://discord.com/"
            )

            embed.add_field(
                name="creatures",
                value=str(disp),
                inline=False
            )

            embed.add_field(
                name="donations",
                value="[Donators get to be a dictator and have special privileges.]("
                      "https://www.patreon.com/join/5133324/checkout)",
                inline=False
            )

            await ctx.send(
                content="",
                embed=embed
            )

            def check(ms):
                return ms.channel == ctx.message.channel and ms.author == ctx.message.author

            character = await self.bot.wait_for('message', check=check)
            self.update_char(ctx.author, character.content)

            return await ctx.send("You are now a " + character.content + ".")

        @self.bot.command(name="gift", description="gifts a player an item", brief="!gift [user] [quantity] [item]",
                          aliases=["gib", "Give", "Gift", "give"],
                          pass_context=True)
        @commands.cooldown(1, 5, commands.BucketType.user)
        async def gift(ctx, member: discord.Member, quantity: int, *, item):
            global itemdict
            item2 = self.sanitize_item(item)
            if member == ctx.author:
                return await ctx.send("Oi! You can't gift yourself.")
            elif item2 not in itemreduce:
                return await ctx.send("That item doesn't even exist lol.")
            elif item2 not in self.get_inv(ctx.author):
                return await ctx.send("Lol you can't gift items you don't have. !buy your friend a gift at the !shop")

            q2 = -quantity
            self.update_inv(ctx.author, item2, q2)
            self.update_inv(member, item2, quantity)
            return await ctx.send("You gave " + member.display_name + " " + str(quantity) + " " + item + "\'s.")

        @self.bot.command(name="mypets", description="shows your pets",
                          brief="!mypets",
                          aliases=[],
                          pass_context=True)
        @commands.cooldown(1, 2, commands.BucketType.user)
        async def mypets(ctx, *, member: discord.Member = None):
            if not member:
                member = ctx.message.author
            embed = discord.Embed(
                title=member.display_name + "'s Pets",
                colour=member.color,
                # url="https://discord.com/"
            )
            embed.set_thumbnail(url=member.avatar_url)
            embed.add_field(
                name=member.display_name + "\'s Pets",
                value=self.disp_pets(member),
                inline=False
            )

            embed.add_field(
                name="donations",
                value="[Donators get to be a dictator and have special privileges.]("
                      "https://www.patreon.com/join/5133324/checkout)",
                inline=False
            )

            await ctx.send(
                content="",
                embed=embed
            )

        @self.bot.command(name="inventory", description="displays user inventory",
                          brief="!inventory *optional - [user]",
                          aliases=["inv", "Inv", "Inventory"],
                          pass_context=True)
        @commands.cooldown(1, 2, commands.BucketType.user)
        async def inventory(ctx, *, member: discord.Member = None):
            if not member:
                member = ctx.message.author
            embed = discord.Embed(
                title=member.display_name + "'s Inventory",
                colour=member.color,
                # url="https://discord.com/"
            )
            embed.set_thumbnail(url=member.avatar_url)
            embed.add_field(
                name="Inventory",
                value=self.disp_inv(member),
                inline=False
            )

            embed.add_field(
                name="donations",
                value="[Donators get to be a dictator and have special privileges.]("
                      "https://www.patreon.com/join/5133324/checkout)",
                inline=False
            )

            await ctx.send(
                content="",
                embed=embed
            )

        @self.bot.command(name="profile", description="displays user profile", brief="!profile *optional - [user]*",
                          aliases=["pf"], pass_context=True)
        @commands.cooldown(1, 2, commands.BucketType.user)
        async def profile(ctx, *, member: discord.Member = None):
            if not member:
                member = ctx.message.author
            embed = discord.Embed(
                title=member.display_name + "'s Profile",
                colour=member.color,
                # url="https://discord.com/",
                description=self.get_occ(member)['occupation'] + " " + self.get_char(member)['creature']
            )
            embed.set_thumbnail(url=member.avatar_url)

            embed.add_field(
                name="Level",
                value=str(self.get_lvl(member)['lvl']),
                inline=True
            )
            embed.add_field(
                name="Experience",
                value=str(self.get_xp(member)['xp']),
                inline=True
            )
            embed.add_field(
                name="Coins Balance",
                value=str(self.get_coin(member)['coin']),
                inline=True
            )
            embed.add_field(
                name="Inventory",
                value=self.disp_inv(member),
                inline=True
            )
            embed.add_field(
                name="Clan",
                value=self.get_clan(member)['clan'],
                inline=True
            )
            embed.add_field(
                name="Pets",
                value=self.disp_pets(member),
                inline=True
            )

            embed.add_field(
                name="donations",
                value="[Donators get to be a dictator and have special privileges.]("
                      "https://www.patreon.com/join/5133324/checkout)",
                inline=False
            )

            await ctx.send(
                content="",
                embed=embed
            )

        @self.bot.command(name="sell", description="sell an item", aliases=["Sell"], brief="!sell [quantity] [item]",
                          pass_context=True)
        @commands.cooldown(1, 5, commands.BucketType.user)
        async def sell(ctx, quantity: int, *, item):
            global itemdict
            item2 = self.sanitize_item(item)
            if item2 not in itemreduce:
                return await ctx.send("That item doesn't even exist lol.")
            elif item2 not in self.get_inv(ctx.author):
                return await ctx.send("Lol you can't sell items you don't have. !buy stuff to sell at the !shop")

            q2 = -quantity
            resell = quantity * ((itemreduce[item2]) / 2)
            self.update_inv(ctx.author, item2, q2)
            self.update_coin(ctx.author, resell)
            return await ctx.send("You sold " + str(quantity) + " " + item + "\'s for " + str(resell) + " coins.")

        @self.bot.command(name="rob", description="attempt to rob coins from a player",
                          brief="!rob [user] [how many coin]",
                          aliases=["Rob"],
                          pass_context=True)
        @commands.cooldown(1, 15, commands.BucketType.user)
        async def rob(ctx, member: discord.Member=None, coins: int=None):

            if member == ctx.author:
                return await ctx.send("You can't rob yourself lol.")

            outcomes = ["success", "failure"]
            outcome = random.choice(outcomes)
            if outcome == "success":
                if self.get_q(ctx.author)['quest'] == "4 Rob someone.":
                    self.update_q(ctx.author, "none")
                    self.update_coin(ctx.author, questlist["4 Rob someone."])
                    await ctx.send("Quest complete! You've been awarded " +
                                   str(questlist["4 Rob someone."]) + " coins!")
                if int(self.get_coin(member)['coin']) <= 0 or int(self.get_coin(member)['coin']) - coins <= 0:
                    return await ctx.send("This person broke, dude.")
                self.update_coin(member, -coins)
                self.update_coin(ctx.author, coins)
                return await ctx.send("You robbed " + member.display_name + " and stole " + str(coins) + " coins.")
            else:
                return await ctx.send("You failed.")

        @self.bot.command(name='8ball',
                          description="Answers a yes/no question.",
                          brief="Answers from the beyond.",
                          aliases=['eight_ball', 'eightball', '8-ball'],
                          pass_context=True)
        async def eight_ball(ctx, *, question=None):
            def check(ms):
                return ms.channel == ctx.message.channel and ms.author == ctx.message.author

            if not question:
                await ctx.send("What do you want to ask 8ball?")
                question2 = await self.bot.wait_for('message', check=check, timeout=10)
                question = question2.content
            possible_responses = [
                'That is a resounding no',
                'It is not looking likely',
                'Ask again',
                'It is quite possible',
                'Definitely',
            ]
            await ctx.send(
                "\"" + question + "\" : " + random.choice(possible_responses) + ", " + ctx.message.author.mention)

        @self.bot.event
        async def on_ready():
            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="you"))
            for guild in self.bot.guilds:
                for member in guild.members:
                    self.add_u_db(member)
            print("{✧} Logged into Discord as " + self.bot.user.name)

        @self.bot.event
        async def on_member_join(member):
            print("{✧} %s has joined the server" % member.id)
            self.add_u_db(member)

        @self.bot.event
        async def on_message(message):
            if message.author.id == 792912391842037822:
                return
            print(str(message.author.id))
            if message.content.lower() == "tell me a joke":
                jokelist = ["I bet I can quit gambling", """Don't trust atoms. They make up everything!""",
                            """Can anyone identify the following:

                                                  Fe - Fe
                                                 /       \\
                                              Fe          Fe
                                                 \\       /
                                                  Fe - Fe

                                        A ferrous wheel""", """To be is to do:               Roussou
                            To do is to be:               Sartre
                                                DO BE DO BE DO BE .... :      Sinatra""", "Why is \"abbreviation\" "
                                                                                          "such a "
                                                                                          "long word?",
                            "Ever stop to think, and forget to start again?",
                            "Don't be so open-minded your brains fall out.", "Look out for #1.  Don't step in #2.",
                            "Shin: A device for finding furniture in the dark.",
                            "My software never has bugs.  It just develops random features.",
                            "Proofread carefully to see if you any words out.",
                            "There are 3 kinds of people: those who can count & those who can't."]
                await message.channel.send(random.choice(jokelist))

            beforelvl = int(self.get_lvl(message.author)['lvl'])
            self.update_xp(message.author, 1)
            petlvllist = []
            if len(self.get_pets(message.author)) > 0 and (list(self.get_pets(message.author)))[0] != "none":
                for x in self.get_pets(message.author):
                    petlvllist.append(self.get_pet_lvl(message.author, x, self.get_pets(message.author)[x])['lvl'])
                    self.update_pet_xp(message.author, self.get_pets(message.author)[x], x, 1)
            await self.bot.process_commands(message)
            afterlvl = int(self.get_lvl(message.author)['lvl'])
            if afterlvl > beforelvl:
                await message.channel.send(message.author.mention + " has leveled up! Check your "
                                                                    "!profile to see what leveling gifts you got.")
                if afterlvl >= 10:
                    if self.get_q(message.author)['quest'] == "2 Get your pet to level 10.":
                        self.update_coin(message.author, questlist["2 Get your pet to level 10."])
                        self.update_q(message.author, "none")
                        await message.channel.send("You completed your quest and received "
                                                   + str(questlist["2 Get your pet to level 10."]) + " coins!")

            if self.get_q(message.author)['quest'] == "6 Get to 100,000 coins.":
                if int(self.get_coin(message.author)['coin']) >= 100000:
                    self.update_coin(message.author, questlist["6 Get to 100,000 coins."])
                    self.update_q(message.author, "none")
                    await message.channel.send("You completed your quest and received "
                                               + str(questlist["6 Get to 100,000 coins."]) + " coins!")

            if self.get_q(message.author)['quest'] == "7 Get to a million coins.":
                if int(self.get_coin(message.author)['coin']) >= 100000:
                    self.update_coin(message.author, questlist["7 Get to a million coins."])
                    self.update_q(message.author, "none")
                    await message.channel.send("You completed your quest and received "
                                               + str(questlist["7 Get to a million coins."]) + " coins!")

            if len(self.get_pets(message.author)) > 0 and (list(self.get_pets(message.author)))[0] != "none":
                count = 0
                for y in self.get_pets(message.author):
                    if int(self.get_pet_lvl(message.author,
                                            y, self.get_pets(message.author)[y])['lvl']) > petlvllist[count]:
                        await message.channel.send("Pet " + y + " named " + self.get_pets(message.author)[y] +
                                                   " has leveled up! Check your "
                                                   "!profile to see what leveling gifts you got.")
                    count += 1

        @self.bot.event
        async def on_command_error(ctx, error):
            if isinstance(error, commands.errors.CommandOnCooldown):
                return await ctx.send("This command is on a %.2fs cooldown" % error.retry_after)

        # log into database on join
        # get xp on message, level up and get coin

        # choose character
        # shop with coins
        # armor
        # Stuff to do:
        # attack ppl
        # rob
        # fight evil
        # get married
        # fishing
        # get job
        # go hunt
        # backpack
        # lootboxes
        # wallet
        # bank
        # stuff
        # pets
        # mini games to get more xp and coin
        # sell stuff
        # gift ppl
        # chances
        # drop items
        # cute pets
        # use
        # leaderboard
        # voting
        # donate real moneys
        # go on quest
        # casino
        # clans
        # profile/stats/rank

    def is_donator(self, member):
        try:
            with self.db.cursor() as cursor:
                sql = "SELECT `isdonator` FROM `players` WHERE user_id = %s"
                cursor.execute(sql, member.id)
                result = cursor.fetchone()
                if not result:
                    print("{✧} User does not exist: %s" % member.id)
                else:
                    if result['isdonator'] == "yes":
                        return True
                    else:
                        return False
        except Exception as e:
            print("{✧} Error with user %s \n%s " % (member.id, e))

    def replace_pet(self, member, petspecies, petname, ps2, pn2):
        self.update_pets(member, petspecies, petname, "remove")
        self.rem_pet_db(member, petspecies, petname)
        self.add_pet_db(member, ps2, pn2)
        self.update_pets(member, ps2, pn2, "add")

    def disp_pets(self, member):
        pets = self.get_pets(member)
        disp = ""
        count = 0
        for y in pets:
            count += 1
            if y == "none":
                return "none"
            if count == len(pets):
                disp += y + " named " + pets[y]
            else:
                disp += y + " named " + pets[y] + ", "
        return disp

    def get_pets(self, member):
        try:
            with self.db.cursor() as cursor:
                sql = "SELECT `pets` FROM `players` WHERE `user_id`=%s"
                cursor.execute(sql, member.id)
                result = cursor.fetchone()
                if not result:
                    print("{✧} User does not exist: %s" % member.id)
                else:
                    resultL = {}
                    if result == {}:
                        resultL = {}
                    else:
                        for x in result['pets'].split(", "):
                            if x == "":
                                continue
                            count = 0
                            holder = ""
                            for y in x.split(' '):
                                count += 1
                                if count == 1:
                                    holder = y
                                    if resultL == {}:
                                        resultL = {y: ""}
                                    else:
                                        resultL.update({y: ""})
                                elif count == 2:
                                    resultL[holder] = y
                                    count = 0

                    return resultL
        except Exception as e:
            print("{✧} Error with id %s.\n%s " % (member.id, e))

    def get_pet_xp(self, member, petspecies, petname):
        try:
            with self.db.cursor() as cursor:
                sql = "SELECT `xp` FROM `pets` WHERE (ownerid, name, species) = (%s, %s, %s)"
                cursor.execute(sql, (member.id, petname, petspecies))
                result = cursor.fetchone()
                if not result:
                    print("{✧} Pet does not exist: %s" % member.id)
                else:
                    return result
        except Exception as e:
            print("{✧} Error with pet %s named %s.\n%s " % (petspecies, petname, e))

    def get_pet_lvl(self, member, petspecies, petname):
        try:
            with self.db.cursor() as cursor:
                sql = "SELECT `lvl` FROM `pets` WHERE (ownerid, name, species) = (%s, %s, %s)"
                cursor.execute(sql, (member.id, petname, petspecies))
                result = cursor.fetchone()
                if not result:
                    print("{✧} Pet does not exist: %s" % member.id)
                else:
                    return result
        except Exception as e:
            print("{✧} Error with pet %s named %s.\n%s " % (petspecies, petname, e))

    def update_pet_lvl(self, member, petspecies, petname, level):
        petlvl = self.get_pet_lvl(member, petspecies, petname)['lvl']
        if level > petlvl:
            with self.db.cursor() as cursor:
                try:
                    sql = "UPDATE `pets` SET `lvl` = %s WHERE (ownerid, name, species) = (%s, %s, %s)"
                    new_lvl = level

                    cursor.execute(sql, (new_lvl, member.id, petname, petspecies))
                    self.db.commit()
                    print("{✧} Updated user %s 's pet's lvl from %s to %s" % (member.id, petlvl, new_lvl))
                except Exception as e:
                    print("{✧} error updating lvl for %s 's pet: %s" % (member.id, e))
        else:
            return

    def update_pet_xp(self, member, petname, petspecies, points):
        l1 = 100
        l2 = 200
        l3 = 500
        l4 = 1000
        l5 = 5000
        l6 = 10000
        l7 = 15000
        l8 = 20000
        l9 = 30000
        l10 = 50000

        petxp = self.get_pet_xp(member, petspecies, petname)['xp']
        with self.db.cursor() as cursor:
            try:
                sql = "UPDATE `pets` SET xp = %s WHERE (ownerid, name, species) = (%s, %s, %s)"
                new_xp = petxp + points
                if new_xp >= l10:
                    self.update_pet_lvl(member, petspecies, petname, 10)
                elif new_xp >= l9:
                    self.update_pet_lvl(member, petspecies, petname, 9)
                elif new_xp >= l8:
                    self.update_pet_lvl(member, petspecies, petname, 8)
                elif new_xp >= l7:
                    self.update_pet_lvl(member, petspecies, petname, 7)
                elif new_xp >= l6:
                    self.update_pet_lvl(member, petspecies, petname, 6)
                elif new_xp >= l5:
                    self.update_pet_lvl(member, petspecies, petname, 5)
                elif new_xp >= l4:
                    self.update_pet_lvl(member, petspecies, petname, 4)
                elif new_xp >= l3:
                    self.update_pet_lvl(member, petspecies, petname, 3)
                elif new_xp >= l2:
                    self.update_pet_lvl(member, petspecies, petname, 2)
                elif new_xp >= l1:
                    self.update_pet_lvl(member, petspecies, petname, 1)

                cursor.execute(sql, (new_xp, member.id, petname, petspecies))
                self.db.commit()
                print("{✧} Updated user %s 's pet's xp from %s to %s" % (member.id, petxp, new_xp))
            except Exception as e:
                print("{✧} error adding xp for %s: %s" % (member.id, e))

    def add_pet_db(self, member, petspecies, petname):
        ownerid = member.id
        name = petname
        xp = 0
        lvl = 0
        species = petspecies
        try:
            with self.db.cursor() as cursor:
                sql = "INSERT INTO `pets` (`ownerid`, `name`, `xp`, `lvl`, `species`) VALUES (%s, %s, %s, %s, %s) "
                cursor.execute(sql, (ownerid, name, xp, lvl, species))
            self.db.commit()
            print("{✧} added " + petspecies + " named " + petname + " to the database")
        except Exception as e:
            print("{✧} error adding pet: %s" % e)

    def rem_pet_db(self, member, petspecies, petname):
        try:
            with self.db.cursor() as cursor:
                sql = "DELETE from `pets` where (`ownerid`, `name`, `species`) = (%s, %s, %s) "
                cursor.execute(sql, (member.id, petname, petspecies))
            self.db.commit()
            print("{✧} deleted " + petspecies + " named " + petname + " from the database")
        except Exception as e:
            print("{✧} error deleting pet: %s" % e)

    def update_pets(self, member, petspecies, petname, addorremove):
        player = self.get_pets(member)
        print(player)
        playerS = ""
        if not player:
            playerS = ""
        else:
            for x in player:
                playerS += x
                playerS += ' ' + player[x] + ", "
        with self.db.cursor() as cursor:
            try:
                sql = "UPDATE players SET pets = %s WHERE user_id = %s"
                if petname == "clear" or petspecies == "clear":
                    new_pets = ""
                else:
                    new_pets = ""
                    if not player:
                        new_pets += (petspecies + ' ' + petname + ", ")
                    else:
                        isThere = False
                        if addorremove == "remove":
                            self.rem_pet_db(member, petspecies, petname)
                            for y in player:
                                if y == petspecies:
                                    if player[y] == petname:
                                        continue
                                new_pets += (y + ' ' + player[y] + ", ")
                        elif addorremove == "add":
                            self.add_pet_db(member, petspecies, petname)
                            for y in player:
                                if y == 'none' and player[y] == '':
                                    continue
                                new_pets += (y + ' ' + player[y] + ", ")
                            new_pets += (petspecies + ' ' + petname + ", ")
                if new_pets == "":
                    new_pets = "none  ,"
                cursor.execute(sql, (new_pets, member.id))
                self.db.commit()
                print("{✧} Updated user %s 's pets from %s to %s" % (member.id, playerS, new_pets))
            except Exception as e:
                print("{✧} error adding pet for %s: %s" % (member.id, e))

    def get_a_user(self):
        memberlist = []
        for member in self.bot.get_all_members():
            memberlist.append(member)
        randmember = memberlist[random.randint(0, len(memberlist) - 1)]
        return randmember

    def get_q(self, member):
        try:
            with self.db.cursor() as cursor:
                sql = "SELECT `quest` FROM `players` WHERE `user_id`=%s"
                cursor.execute(sql, member.id)
                result = cursor.fetchone()
                if not result:
                    print("{✧} User does not exist: %s" % member.id)
                else:
                    return result
        except Exception as e:
            print("{✧} Error with id %s.\n%s " % (member.id, e))

    def update_q(self, member, quest):
        player = self.get_q(member)
        with self.db.cursor() as cursor:
            try:
                sql = "UPDATE players SET quest = %s WHERE user_id = %s"
                new_q = quest
                cursor.execute(sql, (quest, member.id))
                self.db.commit()
                print("{✧} Updated user %s 's quest from %s to %s" % (member.id, player['quest'], new_q))
            except Exception as e:
                print("{✧} error updating quest for %s: %s" % (member.id, e))

    def get_occ(self, member):
        try:
            with self.db.cursor() as cursor:
                sql = "SELECT `occupation` FROM `players` WHERE `user_id`=%s"
                cursor.execute(sql, member.id)
                result = cursor.fetchone()
                if not result:
                    print("{✧} User does not exist: %s" % member.id)
                else:
                    return result
        except Exception as e:
            print("{✧} Error with id %s.\n%s " % (member.id, e))

    def update_occ(self, member, occupation):
        player = self.get_occ(member)
        with self.db.cursor() as cursor:
            try:
                sql = "UPDATE players SET occupation = %s WHERE user_id = %s"
                new_occ = occupation
                cursor.execute(sql, (occupation, member.id))
                self.db.commit()
                print("{✧} Updated user %s 's occupation from %s to %s" % (member.id, player['occupation'], new_occ))
            except Exception as e:
                print("{✧} error updating occupation for %s: %s" % (member.id, e))

    def get_char(self, member):
        try:
            with self.db.cursor() as cursor:
                sql = "SELECT `creature` FROM `players` WHERE `user_id`=%s"
                cursor.execute(sql, member.id)
                result = cursor.fetchone()
                if not result:
                    print("{✧} User does not exist: %s" % member.id)
                else:
                    return result
        except Exception as e:
            print("{✧} Error with id %s.\n%s " % (member.id, e))

    def update_char(self, member, character):
        player = self.get_char(member)
        with self.db.cursor() as cursor:
            try:
                sql = "UPDATE players SET creature = %s WHERE user_id = %s"
                new_char = character
                cursor.execute(sql, (character, member.id))
                self.db.commit()
                print("{✧} Updated user %s 's creature from %s to %s" % (member.id, player['creature'], new_char))
            except Exception as e:
                print("{✧} error updating creature for %s: %s" % (member.id, e))

    def sanitize_item(self, item):
        item = item.lower()
        item = item.replace(' ', '')
        taliases = ["treasurechest", "treasurebox", "treasure"]
        if item in taliases:
            newitem = "treasurebox"
        else:
            newitem = item
        return newitem

    def get_player(self, member):
        try:
            with self.db.cursor() as cursor:
                sql = "SELECT `user_id`, `first_seen`, `xp` FROM `players` WHERE `user_id`=%s"
                cursor.execute(sql, member.id)
                result = cursor.fetchone()
                if not result:
                    print("{✧} User does not exist: %s" % member.id)
                else:
                    return result
        except Exception as e:
            print("{✧} Error with id %s.\n%s " % (member.id, e))

    def clear_pet_db(self, member):
        with self.db.cursor() as cursor:
            try:
                sql = "DELETE FROM pets WHERE ownerid = %s"
                cursor.execute(sql, member.id)
                self.db.commit()
            except Exception as e:
                print("{✧} error clearing pets for %s: %s" % (member.id, e))

    def clear_pets(self, member):
        self.clear_pet_db(member)
        with self.db.cursor() as cursor:
            try:
                sql = "UPDATE players SET pets = %s WHERE user_id = %s"
                new_pets = "none"
                cursor.execute(sql, (new_pets, member.id))
                self.db.commit()
                print("{✧} Cleared pets")
            except Exception as e:
                print("{✧} error clearing pets for %s: %s" % (member.id, e))

    def clear_lvl(self, member):
        player = self.get_lvl(member)
        with self.db.cursor() as cursor:
            try:
                sql = "UPDATE players SET lvl = %s WHERE user_id = %s"
                new_lvl = 0
                cursor.execute(sql, (new_lvl, member.id))
                self.db.commit()
                print("{✧} Updated user %s 's occupation from %s to %s" % (member.id, player['lvl'], new_lvl))
            except Exception as e:
                print("{✧} error updating occupation for %s: %s" % (member.id, e))

    def get_lvl(self, member):
        try:
            with self.db.cursor() as cursor:
                sql = "SELECT `lvl` FROM `players` WHERE `user_id`=%s"
                cursor.execute(sql, member.id)
                result = cursor.fetchone()
                if not result:
                    print("{✧} User does not exist: %s" % member.id)
                else:
                    return result
        except Exception as e:
            print("{✧} Error with id %s.\n%s " % (member.id, e))

    def level_up(self, member, level):
        player = self.get_lvl(member)
        if level > player['lvl']:
            with self.db.cursor() as cursor:
                try:
                    sql = "UPDATE players SET lvl = %s WHERE user_id = %s"
                    new_lvl = level
                    if new_lvl == 10:
                        self.update_inv(member, "treasurebox", 5)
                        self.update_coin(member, 100000)
                    elif new_lvl == 9:
                        self.update_inv(member, "treasurebox", 4)
                        self.update_coin(member, 90000)
                    elif new_lvl == 8:
                        self.update_inv(member, "treasurebox", 3)
                        self.update_coin(member, 80000)
                    elif new_lvl == 7:
                        self.update_inv(member, "treasurebox", 2)
                        self.update_coin(member, 70000)
                    elif new_lvl == 6:
                        self.update_inv(member, "treasurebox", 1)
                        self.update_coin(member, 60000)
                    elif new_lvl == 5:
                        self.update_inv(member, "treasurebox", 1)
                        self.update_coin(member, 5000)
                    elif new_lvl == 4:
                        self.update_inv(member, "treasurebox", 1)
                        self.update_coin(member, 4000)
                    elif new_lvl == 3:
                        self.update_inv(member, "treasurebox", 1)
                        self.update_coin(member, 300)
                    elif new_lvl == 2:
                        self.update_inv(member, "treasurebox", 1)
                        self.update_coin(member, 200)
                    elif new_lvl == 1:
                        self.update_coin(member, 100)
                    cursor.execute(sql, (new_lvl, member.id))
                    self.db.commit()
                    print("{✧} Updated user %s 's lvl from %s to %s" % (member.id, player['lvl'], new_lvl))
                except Exception as e:
                    print("{✧} error updating lvl for %s: %s" % (member.id, e))
        else:
            return

    def get_clan(self, member):
        try:
            with self.db.cursor() as cursor:
                sql = "SELECT `clan` FROM `players` WHERE `user_id`=%s"
                cursor.execute(sql, member.id)
                result = cursor.fetchone()
                if not result:
                    print("{✧} User does not exist: %s" % member.id)
                else:
                    return result
        except Exception as e:
            print("{✧} Error with id %s.\n%s " % (member.id, e))

    def update_clan(self, member, clann):
        player = self.get_clan(member)
        with self.db.cursor() as cursor:
            try:
                sql = "UPDATE players SET clan = %s WHERE user_id = %s"
                new_clan = clann
                cursor.execute(sql, (clann, member.id))
                self.db.commit()
                print("{✧} Updated user %s 's clan from %s to %s" % (member.id, player['clan'], new_clan))
            except Exception as e:
                print("{✧} error updating clan for %s: %s" % (member.id, e))

    def get_inv(self, member):
        try:
            with self.db.cursor() as cursor:
                sql = "SELECT `inv` FROM `players` WHERE `user_id`=%s"
                cursor.execute(sql, member.id)
                result = cursor.fetchone()
                if not result:
                    print("{✧} User does not exist: %s" % member.id)
                else:
                    resultL = {}
                    if result == {}:
                        resultL = {}
                    else:
                        for x in result['inv'].split(", "):
                            if x == "":
                                continue
                            count = 0
                            holder = ""
                            for y in x.split(' '):
                                count += 1
                                if count == 1:
                                    holder = y
                                    if resultL == {}:
                                        resultL = {y: ""}
                                    else:
                                        resultL.update({y: ""})
                                elif count == 2:
                                    resultL[holder] = y
                                    count = 0

                    return resultL
        except Exception as e:
            print("{✧} Error with id %s.\n%s " % (member.id, e))

    def disp_inv(self, member):
        i = self.get_inv(member)
        idisp = ""
        for x in i:
            if x == "treasurebox":
                idisp += "treasure box"
            else:
                idisp += x
            idisp += ": " + i[x] + "\n"
        return idisp

    def update_inv(self, member, item, quantity):
        player = self.get_inv(member)
        print(player)
        playerS = ""
        if not player:
            playerS = ""
        else:
            for x in player:
                playerS += x
                playerS += ' ' + player[x] + ", "
        with self.db.cursor() as cursor:
            try:
                sql = "UPDATE players SET inv = %s WHERE user_id = %s"
                if item == "clear":
                    new_inv = "none"
                else:
                    new_inv = ""
                    if not player:
                        new_inv += (item + ' ' + str(quantity) + ", ")
                    else:
                        isThere = False
                        for y in player:
                            if y == "none":
                                continue
                            if player == "":
                                continue
                            if y == item:
                                isThere = True
                                new_q = int(player[y]) + quantity
                                if new_q < 1:
                                    continue
                                else:
                                    new_inv += (item + ' ' + str(new_q) + ", ")
                            else:
                                new_inv += (y + ' ' + str(player[y]) + ", ")
                        if not isThere:
                            new_inv += (item + ' ' + str(quantity) + ", ")
                if new_inv == "":
                    new_inv = "none"

                cursor.execute(sql, (new_inv, member.id))
                self.db.commit()
                print("{✧} Updated user %s 's inv from %s to %s" % (member.id, playerS, new_inv))
            except Exception as e:
                print("{✧} error adding item for %s: %s" % (member.id, e))

    def get_coin(self, member):
        try:
            with self.db.cursor() as cursor:
                sql = "SELECT `coin` FROM `players` WHERE `user_id`=%s"
                cursor.execute(sql, member.id)
                result = cursor.fetchone()
                if not result:
                    print("{✧} User does not exist: %s" % member.id)
                else:
                    return result
        except Exception as e:
            print("{✧} Error with id %s.\n%s " % (member.id, e))

    def update_coin(self, member, coins):
        player = self.get_coin(member)
        with self.db.cursor() as cursor:
            try:
                sql = "UPDATE players SET coin = %s WHERE user_id = %s"
                new_coin = player['coin'] + coins
                cursor.execute(sql, (player['coin'] + coins, member.id))
                self.db.commit()
                print("{✧} Updated user %s 's coins from %s to %s" % (member.id, player['coin'], new_coin))
            except Exception as e:
                print("{✧} error adding coins for %s: %s" % (member.id, e))

    def get_xp(self, member):
        try:
            with self.db.cursor() as cursor:
                sql = "SELECT `xp` FROM `players` WHERE `user_id`=%s"
                cursor.execute(sql, member.id)
                result = cursor.fetchone()
                if not result:
                    print("{✧} User does not exist: %s" % member.id)
                else:
                    return result
        except Exception as e:
            print("{✧} Error with id %s.\n%s " % (member.id, e))

    def update_xp(self, member, points):
        l1 = 100
        l2 = 200
        l3 = 500
        l4 = 1000
        l5 = 5000
        l6 = 10000
        l7 = 15000
        l8 = 20000
        l9 = 30000
        l10 = 50000

        player = self.get_xp(member)
        with self.db.cursor() as cursor:
            try:
                sql = "UPDATE players SET xp = %s WHERE user_id = %s"
                new_xp = player['xp'] + points
                if new_xp >= l10:
                    self.level_up(member, 10)
                elif new_xp >= l9:
                    self.level_up(member, 9)
                elif new_xp >= l8:
                    self.level_up(member, 8)
                elif new_xp >= l7:
                    self.level_up(member, 7)
                elif new_xp >= l6:
                    self.level_up(member, 6)
                elif new_xp >= l5:
                    self.level_up(member, 5)
                elif new_xp >= l4:
                    self.level_up(member, 4)
                elif new_xp >= l3:
                    self.level_up(member, 3)
                elif new_xp >= l2:
                    self.level_up(member, 2)
                elif new_xp >= l1:
                    self.level_up(member, 1)

                cursor.execute(sql, (player['xp'] + points, member.id))
                self.db.commit()
                print("{✧} Updated user %s 's xp from %s to %s" % (member.id, player['xp'], new_xp))
            except Exception as e:
                print("{✧} error adding xp for %s: %s" % (member.id, e))


if __name__ == '__main__':
    bot = RPGLion(BOT_TOKEN)
    bot.run()
