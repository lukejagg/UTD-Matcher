import difflib

from asyncio import Task
import random
import asyncio
import os
import discord
from discord.ext import commands









player1 = ""
player2 = ""
turn = ""
gameOver = True

board = []

winningConditions = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
]




TOKEN = TOKEN or os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix='!')












hanggames = {}

class Hangman:
    word = ""
    progress_word = ""
    guesses = list()
    max_guesses = 10

    def __init__(self, word):
        self.word = word
        self.guesses = list()

    def is_game_over(self, guess):
        game_over = False
        won = False

        if self.check_guesses_left() == 0:
            game_over = True

        won = self.check_word_guess(guess)

        if won:
            game_over = True
        return game_over, won

    def get_number_of_guesses(self):
        return len(self.guesses)

    def check_guesses_left(self):
        if self.get_number_of_guesses() >= self.max_guesses:
            return 0
        return self.max_guesses - self.get_number_of_guesses()

    def check_word_guess(self, word):
        if self.word == word:
            return True
        return False

    def guess(self, character):
        character = character.lower()

        self.progress_word = ""

        for c in self.word.lower():
            if character == c or c in self.guesses:
                self.progress_word += c
            else:
                self.progress_word += "\_."

        self.guesses.append(character)

class HangmanGame:
    current_game = None

    def get_secret_word(self):
        return self.current_game.word

    def get_guess_string(self):
        return ",".join(self.current_game.guesses)

    def get_progress_string(self):
        return self.current_game.progress_word

    def run(self, player_id, guess):
        self.get_game(player_id)
        is_game_over, won = self.play_round(guess)
        self.save(player_id)
        return is_game_over, won

    def play_round(self, guess):
        is_word = False
        if len(guess) == 1:
            pass
        elif len(guess) > 1:
            is_word = True
        else:
            return None, None

        if not is_word:
            self.current_game.guess(guess)

        is_game_over, won = self.current_game.is_game_over(guess)
        return is_game_over, won

    def get_game(self, player_id):
        if player_id in hanggames.keys():
            self.current_game = hanggames[player_id]
            if self.current_game is None:
                self.create_game(player_id)
        else:
            self.create_game(player_id)

    def get_random_word(self):
        return random.choice(('discord', 'bot', 'ultimate', 'python', 'development'))

    def create_game(self, player_id):
        self.current_game = Hangman(self.get_random_word())
        self.save(player_id)

    def save(self, player_id):
        hanggames[player_id] = self.current_game

    async def reset(self, player_id):
        hanggames.pop(player_id)




























@bot.command()
async def tictactoe(ctx, p1: discord.Member, p2: discord.Member):
    global count
    global player1
    global player2
    global turn
    global gameOver

    if gameOver:
        global board
        board = [":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:"]
        turn = ""
        gameOver = False
        count = 0

        player1 = p1
        player2 = p2

        # print the board
        line = ""
        t = ""
        for x in range(len(board)):
            if x == 2 or x == 5 or x == 8:
                line += " " + board[x]
                t += line + "\n"
                line = ""
            else:
                line += " " + board[x]
        t = t.replace("\n ", "\n")
        await ctx.send(t)

        # determine who goes first
        num = random.randint(1, 2)
        if num == 1:
            turn = player1
            await ctx.send("It is <@" + str(player1.id) + ">'s turn.")
        elif num == 2:
            turn = player2
            await ctx.send("It is <@" + str(player2.id) + ">'s turn.")
    else:
        await ctx.send("A game is already in progress! Finish it before starting a new one.")


@bot.command()
async def place(ctx, pos: int):
    global turn
    global player1
    global player2
    global board
    global count
    global gameOver

    if not gameOver:
        mark = ""
        if turn == ctx.author:
            if turn == player1:
                mark = ":regional_indicator_x:"
            elif turn == player2:
                mark = ":o2:"
            if 0 < pos < 10 and board[pos - 1] == ":white_large_square:" :
                board[pos - 1] = mark
                count += 1

                # print the board
                line = ""
                t = ""
                for x in range(len(board)):
                    if x == 2 or x == 5 or x == 8:
                        line += " " + board[x]
                        t += line + "\n"
                        line = ""
                    else:
                        line += " " + board[x]
                t = t.replace("\n ", "\n")
                await ctx.send(t)

                checkWinner(winningConditions, mark)
                print(count)
                if gameOver == True:
                    await ctx.send(mark + " wins!")
                elif count >= 9:
                    gameOver = True
                    await ctx.send("It's a tie!")

                # switch turns
                if turn == player1:
                    turn = player2
                elif turn == player2:
                    turn = player1
            else:
                await ctx.send("Be sure to choose an integer between 1 and 9 (inclusive) and an unmarked tile.")
        else:
            await ctx.send("It is not your turn.")
    else:
        await ctx.send("Please start a new game using the !tictactoe command.")


def checkWinner(winningConditions, mark):
    global gameOver
    for condition in winningConditions:
        if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark:
            gameOver = True


@tictactoe.error
async def tictactoe_error(ctx, error):
    print(error)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please mention 2 players for this command.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Please make sure to mention/ping players (ie. <@835303314883215360>).")


@place.error
async def place_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please enter a position you would like to mark.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Please make sure to enter an integer.")





#######################################
# Settings

emoji = '👍'
games = ['game','minecraft','potato','tic tac toe','alone']
game_data = {
    'game': {'players':4},
    'minecraft': {'players':2},
    'potato': {'players':3},
    'tic tac toe': {'players': 2},
    'alone': {'players': 1},
}

########################################

#########################################
# INTERNAL STORAGE

# counter[guild] = num
counter = {}

# requests[message] = { type = 'chat', max = 5, etc... }
chat_requests = {}

# requests[message] = { type = 'chat', max = 5, etc... }
voice_requests = {}

# group[channel id] =
chat_groups = {}


# PROMPTS
x = open("questions.txt", 'r')
questions = x.readlines()
x.close()

def get_prompt():
    """gives prompts if commanded w/ !prompt"""
    return random.choice(questions)


# VOICE CHANNELS
def get_voice_channels(guild):
    return


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------------------')

# GAMES
@bot.command()
async def game(ctx, *gamestr):
    """Adds two numbers together."""
    desc = ' '.join(gamestr)
    g = difflib.get_close_matches(desc, games)
    if (len(g) == 0):
        await ctx.send("Game not found...")
        return

    g = g[0]
    maxPeople = (game_data[g])['players']
    data = {"type": "game", "max": maxPeople, "game": g}

    embed = discord.Embed(title=f"Game Room ({maxPeople})", description=f"Anyone want to play {g}?", color=0xFF5733)
    # embed.add_field(name='Created By', value=f'<@{ctx.author.id}>')
    msg = await ctx.send(embed=embed)
    chat_requests[msg] = data
    await msg.add_reaction(emoji)


##################### TEXT CHANNELS
def get_num(guild):
    counter[guild] = counter.get(guild, 0) + 1
    return counter[guild]

@bot.event
async def on_reaction_add(reaction, user: discord.Member):
    if reaction.emoji == emoji:
        if reaction.message in chat_requests:
            r = chat_requests[reaction.message]
            if reaction.count - 1 >= r['max']:
                users = await reaction.users().flatten()
                called = reaction.message.channel
                del users[0]
                del chat_requests[reaction.message]
                g = reaction.message.guild
                overwrites = {
                    g.default_role: discord.PermissionOverwrite(read_messages=False),
                    g.me: discord.PermissionOverwrite(read_messages=True),
                }
                channel = await g.create_text_channel(f"chat{get_num(g)}", overwrites=overwrites)
                chat_groups[channel] = {"users": users, "called": called}
                delete_delay(channel)
                pings = ""
                for a in users:
                    pings += f"<@{a.id}>"
                    p = channel.overwrites_for(a)
                    p.send_messages = True
                    p.read_messages = True
                    await channel.set_permissions(a, overwrite=p)
                pings += "\n"

                if r['type'] == 'game':
                    await channel.send(pings + f'Get ready to play {r["game"]}!')

                    if r['game'] == 'tic tac toe':
                        await channel.send("!place 1-9 (e.g. !place 1)")
                        await tictactoe(channel, users[0], users[1])
                else:
                    await channel.send(pings + get_prompt())


async def delete_coroutine(channel):
    await asyncio.sleep(240)
    await channel.send("Anyone want to add anything else?")
    await asyncio.sleep(60)
    users = (chat_groups[channel])['users']
    pings = ""
    for a in users:
        pings += f"<@{a.id}> "
    await (chat_groups[channel])['called'].send(pings + "\nThe chat has been closed. I hope you had a good discussion!")
    del chat_groups[channel]
    await channel.delete()


def delete_delay(channel):
    if channel not in chat_groups:
        return

    c = chat_groups[channel]
    if 'delete' in c:
        Task.cancel(c['delete'])
    task = asyncio.create_task(delete_coroutine(channel))
    c["delete"] = task


matches = {}
meets = []
match_queue = None

async def match(ctx):
    global match_queue

    id = ctx.author
    if match_queue is None:
        match_queue = id
        await id.dm_channel.send("Finding a match...")
    else:
        id2 = match_queue
        match_queue = None

        matches[id] = id2
        matches[id2] = id

        await id.dm_channel.send("You have been matched. Say hi!\n!quit to exit. !meet to DM.")
        await id2.dm_channel.send("You have been matched. Say hi!\n!quit to exit. !meet to DM.")

        pass


def quit(ctx):
    if match_queue == None:
        pass
    else:
        pass


@bot.event
async def on_message(msg):
    if msg.channel in chat_groups and msg.author.id != 835303314883215360:
        delete_delay(msg.channel)

    id = msg.author
    if msg.author.id != 835303314883215360 and isinstance(msg.channel, discord.channel.DMChannel):
        text = msg.content.lower()
        if text == "!match":
            await match(msg)
        elif text == "!quit":
            if id not in matches:
                return

            id2 = matches[id]
            del matches[id]
            del matches[id2]
            if id in meets:
                meets.remove(id)
            if id2 in meets:
                meets.remove(id2)

            await id2.dm_channel.send(f"**The other person has left.** Say !match to find a new match.")
            await id.dm_channel.send(f"**You left.** Say !match to find a new match")
        elif text == "!meet":
            if id not in matches:
                return

            id2 = matches[id]
            if id not in meets:
                meets.append(id)

            if id in meets and id2 in meets:
                await id.dm_channel.send(f"<@{id2.id}>")
                await id2.dm_channel.send(f"<@{id.id}>")
            else:
                await id2.dm_channel.send(f"The other person wants to know who you are. Say !meet if you want to know who they are.")

        else:
            if id in matches:
                id2 = matches[id]
                await id2.dm_channel.send(msg.content)
            return
    else:
        await bot.process_commands(msg)


@bot.command()
async def chat(ctx, maxPeople: int, *description):
    """Adds two numbers together."""
    desc = ' '.join(description)
    maxPeople = max(1, min(20, maxPeople))
    data = {"type": "chat", "max": maxPeople, "desc": desc}

    embed = discord.Embed(title=f"Chat Room ({maxPeople})", description=len(description) > 0 and desc or "Anyone want to hang out?", color=0xFF5733)
    # embed.add_field(name='Created By', value=f'<@{ctx.author.id}>')
    msg = await ctx.send(embed=embed)
    chat_requests[msg] = data
    await msg.add_reaction(emoji)


##################### VOICE CHANNELS
@bot.event
async def on_voice_state_update(member, before, after):
    if before.channel is None and after.channel is not None:
        if after.channel.id == True:
            pass

####################################
@bot.command()
async def lucas(ctx):
    """easter egg"""
    await ctx.send("<@237059748250255361>")
    await ctx.send("ur dum")


bot.run(TOKEN)
