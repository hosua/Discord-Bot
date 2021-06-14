import os
import discord
import asyncio
from discord.ext import commands
from dotenv import load_dotenv
from Text_generator import Text_Gen
from Name_generator import Name_Generator
from Phrase_maker import Phrase_Maker
from Rock_paper_scissors import Rock_Paper_Scissors
from Product_calculator import Product_Calculator
from Googler import Google_search
from Youtube_searcher import Youtube_Searcher
from Equation_solver import Equation_Solver
from discord.ext.commands import has_permissions, MissingPermissions
import youtube_dl
import random

es = Equation_Solver()
yout = Youtube_Searcher()
goog =  Google_search()
pc = Product_Calculator()
rps = Rock_Paper_Scissors()
tg = Text_Gen()
ng = Name_Generator()
pm = Phrase_Maker("random_adjectives.txt", "random_nouns.txt")
bot = commands.Bot(command_prefix="!")
load_dotenv("token.env")
TOKEN = os.getenv("DISCORD_TOKEN")
players = {}
queue = []
songs = asyncio.Queue()
play_next_song = asyncio.Event()
queues = {} #new dictionary
queues = {} #new dictionary
#queue.append('https://www.youtube.com/watch?v=bPs0xFd4skY') # TEST
#queue.append('https://www.youtube.com/watch?v=ZCu2gwLj9ok')
# Made by Hoswoo, with many implementations by others. This code is horrible, and should not be recreated.
# Source: https://github.com/RK-Coding/Videos/blob/master/rkcodingmusicqueue.py
ytdl_format_options = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192'
    }]
}
ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': False,
    'no_warnings': True,
    'default_search': 'auto',

    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192'
    }],

    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):

        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        f_stripped = filename.rsplit(".", 1)[0] + ".mp3"   # Since I converted this to .mp3 I need to return the correct filename.
        return cls(discord.FFmpegPCMAudio(f_stripped, **ffmpeg_options), data=data)
    @classmethod
    async def from_name(cls, text, *, loop=None, stream=False):
        url = yout.get_first_link(text)
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


@bot.event
async def on_ready():
    print("{0.user} is now operational".format(bot))
@bot.event   # Text checker
async def on_message(ctx):
    await bot.process_commands(ctx)
    if ctx.author == bot.user:   # don't reply to self
        return
    if ctx.content.lower().startswith('hello') or ctx.content.lower().startswith('hi'):
        await ctx.reply("Hello!", mention_author=True)
    if ctx.content.lower().startswith('bye') or ctx.content.lower().startswith('goodbye') or  \
            ctx.content.lower().startswith('good bye') or ctx.content.lower().startswith('bai'):
        await ctx.reply("Goodbye!", mention_author=True)
    if ctx.content.lower().startswith('im gay') or ctx.content.lower().startswith("i'm gay") or \
            ctx.content.lower().startswith("ur gay") or ctx.content.lower().startswith("you're gay") or \
            ctx.content.lower().startswith("youre gay") or ctx.content.lower().startswith("gay"):
        await ctx.reply(ctx.author.name + " is gay!", mention_author=True)
    if ctx.content.lower().startswith("uwu"):
        await ctx.reply("What's this?", mention_author=True)
    if ctx.content.startswith("69"):
        await ctx.reply("Nice.", mention_author=True)
    if ctx.content.lower().startswith("marco"):
        await ctx.reply("Polo!", mention_author=True)
    if ctx.content.lower().startswith("fuck you") or ctx.content.lower().startswith("fuckyou"):
        await ctx.reply("...rude.", mention_author=True)

@bot.command(help="!youtube 'hot dog' # This will return the first # links")
async def youtube(ctx, arg1, arg2=1):
    try:
        await ctx.reply(yout.search(arg1, arg2))
    except discord.errors.HTTPException and IndexError:
        await ctx.reply("You entered too many queries!")


@bot.command(help="!play 'title' or !play 'https://www.youtube.com/' link")
async def play(ctx, arg=None, link=None):
    global queue
    try:
        await join(ctx)
    except:
        pass

    server = ctx.message.guild
    voice = discord.utils.get(bot.voice_clients, guild=server)
    voice_channel = server.voice_client
    try:
        if voice.is_playing():
            await ctx.reply("I'm already playing something!")
            return
        async with ctx.typing():
            if arg==None:   # If we have no argument, just play what's in the queue
                try:
                    player = await YTDLSource.from_url(queue[0], loop=bot.loop)
                    voice_channel.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
                    player.volume = .1
                    await ctx.send('**Now playing:** {}'.format(player.title))
                    del (queue[0])
                except IndexError:
                    player = None
                    await ctx.reply("There's nothing to play.\nTry to **!queue \"song\"** first!")
                except AttributeError:
                    await ctx.reply("I couldn't do that! Type **!join** if I'm not in the channel yet.")
            elif not arg==None and link==None:  # If we have an argument that is not a link
                try:
                    player = await YTDLSource.from_url(queue[0], loop=bot.loop)
                    voice_channel.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
                    player.volume = .1
                    await ctx.send('**Now playing:** {}'.format(player.title))
                    del (queue[0])
                except IndexError:
                    player = None
                    await ctx.reply("There's nothing to play.\nTry to !queue \"song\" first!")
                except AttributeError:
                    await ctx.reply("I couldn't do that! Type **!join** if I'm not in the channel yet.")
    except AttributeError:
        await ctx.reply("Either there are no songs queued, or I'm not in the channel."
                        "\nUse **!join** to join the channel and **!queue \"song\"** to add a song to the queue!")

@bot.command(hidden=True)
async def test_playlist(ctx):
    queue_lst = ["glory days - tia","illenium fractures", "ncs invisible", "okaerinasai tomoatomerde",
"fly away - nanahira", "my dearest - supercell", "blue - mitis", "eos - ginkiha", "anemoi - ginkiha"]
    for item in queue_lst:
        queue.append(item)
    await ctx.reply("Added the test playlist to queue!")
@bot.command(help="!purge # Delete previous # of comments. Default 30, max 100.")
@has_permissions(administrator=True)
async def purge(ctx, amount=30):
    if amount <= 100:
        await ctx.send(f"Are you sure? (y/n)")
        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel and \
                   msg.content.lower() in ["y", "n"]
        msg = await bot.wait_for("message", check=check)


        if msg.content.lower() == "y":
            channel = ctx.message.channel
            messages = []
            async for message in channel.history(limit=amount):
                      messages.append(message)
            await channel.delete_messages(messages)
            await ctx.send(f'{amount} messages have been purged by {ctx.message.author.mention}')
        else:
            await ctx.reply("Okay, I won't do that.")
    else:
        await ctx.reply("Discord will only allow me to do 100 at a time!")

@bot.command(help="Skip the current song")
async def skip(ctx):
    await stop(ctx)
    await play(ctx)
@bot.command(name='queue', help='Can queue titles or youtube links.')
async def queue_(ctx, url):
    global queue
    try:
        await join(ctx)

    except:
        await ctx.reply("I tried joining a voice channel but you're not in one!")
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    queue.append(url)
    await ctx.send(f'`{url}` added to queue!')
    if not voice.is_playing():
        await play(ctx)
@bot.command(help='Show the queue')
async def show_queue(ctx):
    rtn_str = ""
    for i in range(len(queue)):
        rtn_str += str(i+1) + ". " + queue[i] + "\n"
    await ctx.send(f'Your queue is now \n`{rtn_str}`')

@bot.command(name='remove', help='!remove # Remove song from queue at given index')

async def remove_(ctx, number):
    global queue
    rtn_str =""
    try:
        del (queue[int(number)-1])
        for i in range(len(queue)):
            rtn_str += str(i+1) + ". " + queue[i] + "\n"
        await ctx.send(f'Your queue is now \n`{rtn_str}`')
    except:
        await ctx.send('Index was either out of range or your queue is empty!')
        pass

@bot.command(help='!remove # Remove song from queue at given index')
async def clear(ctx):
    global queue
    print("Queue was cleared.")
    queue.clear()
    await ctx.send(f'Your queue is now empty!')

@bot.command(help="Have bot join channel")
async def join(message):
    if message.author == bot.user:
        return
    channel = message.author.voice.channel
    voice = discord.utils.get(bot.voice_clients, guild=message.guild)
    if voice and voice.is_connected():
        return voice, voice.source
    else:
        voice = await channel.connect()  # This causes a random error
        voice.source = discord.PCMVolumeTransformer(voice.source, volume=1)
        await ctx.reply("Joined " + channel + "!")
        print(f"The bot has connected to {channel}\n")

    return voice, voice.source
@bot.command(help="Make bot leave voice channel")
async def leave(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if not voice == None:
        await voice.disconnect()
    else:
        await ctx.reply("I'm not in the voice channel!")
@bot.command(help="Pause the audio")
async def pause(ctx):
    server = ctx.message.guild
    voice_channel = server.voice_client
    if not voice_channel == None:
        voice_channel.pause()
    else:
        await ctx.reply("I'm not playing anything!")
@bot.command(help="Resume the audio")
async def resume(ctx):
    try:
        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        if voice.is_paused():
            voice.resume()
            await ctx.reply("Resuming the song.")
        else:
            await ctx.reply("I'm already playing that!")
    except:
        await ctx.reply("I can't do that right now.")
#@bot.command(help="")
#async def queue(ctx, url):

@bot.command(help="Stop the audio")
async def stop(ctx):


    try:
        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        if voice.is_playing():
            voice.stop()
            await ctx.reply("Stopped playing the song.")
            for file in os.listdir("./"):
                if file.endswith(".mp3"):
                    os.remove(file)
                    print("removed " + file)
        else:
            await ctx.reply("I wasn't playing anything!")
    except:
        await ctx.reply("I can't do that right now.")
@bot.command(help="!google 'hot dog' # This will return the first # links")
async def google(ctx, arg1, arg2=1):
    try:
        await ctx.reply(goog.search(arg1, arg2))
    except discord.errors.HTTPException and IndexError:
        await ctx.reply("You entered too many queries!")
@bot.command(help="!vol # Change volume (0-100)")
async def vol(ctx, volume: float):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)

    if 0 <= volume <= 100:
        if voice.is_playing():
            new_volume = volume / 100
            voice.source.volume = new_volume
            await ctx.reply(f"Changed the volume to {volume}")
    else:
        await ctx.reply("Number must be between 0 and 100")

    #

@bot.command(help="!ping Get latency")
async def ping(ctx):
    await ctx.reply('Pong! {0}'.format(round(bot.latency * 1000)) + "ms")
@bot.command(help="!roll # Roll a number from 0 to # (default 100)")
async def roll(ctx, arg=None):
    if arg == None:
        arg = 100
    await ctx.reply("You rolled: " + str(random.randint(0, int(arg))) + "")
""" Calculator stuff """
@bot.command(hidden=True, administrator=True)
async def help420(ctx):
    help_txt = "\n***Do not include anything that is bolded when typing the commands.***" \
               "\nCommand examples:\n!price 40 ***Returns the cost whilst omitting the profit.***" \
               "\n!use_equations 45 ***Pay***\n!pickup_calc 800 700 " \
               "***Jim's earnings first, then Josh's***\n!own_prices 3.5 45 ***Amount first, then pay***"
    await ctx.reply(help_txt)
@bot.command(hidden=True)
async def price(ctx, arg):
    await ctx.reply(pc.use_equations(arg, True))  # omit profits
@bot.command(hidden=True, administrator=True)
async def use_equations(ctx, arg):
    await ctx.reply(pc.use_equations(arg))
@bot.command(hidden=True, administrator=True)
async def pickup_calc(ctx, arg1, arg2):
    await ctx.reply(pc.pickup_calc(float(arg1), float(arg2)))
@bot.command(hidden=True, administrator=True)
async def own_prices(ctx, arg1, arg2):
    await ctx.reply(pc.own_prices(float(arg1), float(arg2)))
@bot.command(hidden=True)
async def equals(ctx, arg):
    await ctx.reply(eval(arg))
@bot.command(help="!solve 4*x+y x Solve algebra problem")
async def solve(ctx, arg1, arg2=None):
    try:
        await ctx.reply("```" + es.solve(arg1, arg2) + "```") # Put stuff in code blocks if you want to ignore formatting
        if arg1 == None:
            await ctx.reply("Syntax error. Make sure you are using \* when multiplying.")
    except:
        await ctx.reply("There was a syntax error. Make sure you are using \* when multiplying.")
""" Rock paper scissors """
@bot.command(help="!rock Play rock")
async def rock(ctx):
    await ctx.reply(rps.rockPaperScissors("rock"))
@bot.command(help="!paper play paper")
async def paper(ctx):
    await ctx.reply(rps.rockPaperScissors("paper"))
@bot.command(help="!scissors play scissors")
async def scissors(ctx):
    await ctx.reply(rps.rockPaperScissors("scissors"))
""" Text randomizers"""
@bot.command(help="!r_name Generate a random name")
async def r_name(ctx):
    await ctx.reply(ng.generate_random())
@bot.command(help="!r_sentence Generate a random sentence")
async def r_sentence(ctx):
    await ctx.reply(tg.sentence_generator())
@bot.command(help="!r_sentence Generate a random paragraph")
async def r_paragraph(ctx):
    await ctx.reply(tg.rand_paragraph(random.randint(15,25)))
@bot.command(help="!r_sentence Generate a random phrase")
async def r_phrase(ctx):
    await ctx.reply(pm.generate_random())

bot.run(TOKEN)