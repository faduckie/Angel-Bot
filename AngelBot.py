import discord
from discord.ext import commands
import random
import youtube_dl
import asyncio

bot = commands.Bot(command_prefix = '~')
players = {}

@bot.event
async def on_ready():
    print("The bot is ready!")
    
#bot says hello
@bot.command(brief="Angel Bot says hello!")
async def hello(ctx):
    await ctx.send("Hello")

#bot repeats what its told
@bot.command(brief="repeats what you say")
async def say(ctx, *arg):
    string = ""
    for word in arg:
        string += word + " "
    await ctx.send(string)

########################
#DND DICE
@bot.command(brief="rolls d20 with/without modifer")
async def rolld20(ctx, modifier:int = 0)-> None:
    await ctx.send(random.randint(1,20) + modifier)

@bot.command(brief="rolls d12 with/without modifer")
async def rolld12(ctx, modifier: int = 0) -> None:
    await ctx.send(random.randint(1,12) + modifier)

@bot.command(brief="rolls d10 with/without modifer")
async def rolld10(ctx, modifier: int = 0) -> None:
     await ctx.send(random.randint(1,10) + modifier)

@bot.command(brief="rolls d8 with/without modifer")
async def rolld8(ctx, modifier: int = 0) -> None:
     await ctx.send(random.randint(1,8) + modifier)

@bot.command(brief="rolls d6 with/without modifer")
async def rolld6(ctx, modifier: int = 0) -> None:
     await ctx.send(random.randint(1,6) + modifier)

@bot.command(brief="rolls d4 with/without modifer")
async def rolld4(ctx, modifier:int = 0)-> None:
     await ctx.send(random.randint(1,4) + modifier)
############################



#voice channel stuff#
##############################
@bot.command(brief="joins voice channel")
async def join(ctx):
    channel = ctx.author.voice.channel
    global vc
    vc = await channel.connect()

@bot.command(brief="leaves the voice channel")
async def leave(ctx):
    await ctx.voice_client.disconnect()

songs = asyncio.Queue()
playNextSong = asyncio.Event()

async def audioPlayTask():
    while True:
        playNextSong.clear()
        current = await songs.get()
        current.start()
        await playNextSong.wait()

@bot.command(brief="plays songs when bot is in VC", description="plays a song in VC given a url & provided that the bot is in the VC")
async def play(ctx, url):
    ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
                }],
            }
    meta = youtube_dl.YoutubeDL(ydl_opts).extract_info(url)
    title = meta["title"].strip() + "-" + meta['id'] + ".mp3"
    
    try:
        vc.play(discord.FFmpegPCMAudio(title), after=lambda e: print('done',e))
    except:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        vc.play(discord.FFmpegPCMAudio(title), after=lambda e: print('done',e))
    

################################

#Helpful d&d links
    
@bot.command(brief="Displays link to the Player's Handbook")
async def phb(ctx):
    await ctx.send("https://thetrove.net/Books/Dungeons%20&%20Dragons/5th%20Edition%20(5e)/Core/Player%27s%20Handbook%20%5B10th%20Print%5D.pdf")

@bot.command(brief="Displays link to character creation ideas")
async def characterIdeas(ctx):
    await ctx.send("http://whothefuckismydndcharacter.com/")

@bot.command(brief="Displays link to possible puzzles the DM could use")
async def puzzles(ctx):
    await ctx.send("https://tvtropes.org/pmwiki/pmwiki.php/Main/StockVideoGamePuzzle")
    
@bot.command(brief="Displays link to store inventory generator")
async def storeGen(ctx):
    await ctx.send("https://www.realmshelps.net/stores/store.shtml")
    

    
bot.run('NzQ2MTg0NTA1MjQ4OTcyOTEw.Xz8oeQ.hAwFzC2phpixYzww-gcd-MSqw5w')

@bot.command(name='logout')
async def _logout(ctx):
  await bot.logout()

