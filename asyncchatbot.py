from twitchio.ext import commands
import time
import aiohttp
import ast
import os

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

unlocked = False
twitchtoken = os.environ.get('TWITCHTOKEN')
twitchusername = os.environ.get('TWITCHUSERNAME')
twitchchannel = os.environ.get('TWITCHCHANNEL')


class Bot(commands.Bot):

    def __init__(self):
        super().__init__(irc_token=twitchtoken, nick=twitchusername, prefix='!',
                         initial_channels=[twitchchannel])

    # Events don't need decorators when subclassed
    async def event_ready(self):
        print(f'Ready | {self.nick}')

    async def event_message(self, message):
        await self.handle_commands(message)

    # Commands use a different decorator
    @commands.command(name='buy')
    async def do_buy(self, ctx):
        if unlocked:
            if not ctx.content.count(" ") == 2:
                await ctx.send(f'Usage: !buy <Ticker> <Number of Shares>')
            else:
                ticker = ctx.content.split(" ")[1]
                amount = ctx.content.split(" ")[2]
                try:
                    int(amount)
                    username = ctx.author.name
                    async with aiohttp.ClientSession() as session:
                        r = await fetch(session, "http://localhost:8000/api/stock/" + ticker + "/buy/" + amount + "/user/" + username)
                        if r != '"Trade Successful"':
                            await ctx.send(f'@{ctx.author.name}: ' + r)
                except Exception as e:
                    await ctx.send(f'Usage: !buy <Ticker> <Number of Shares>')

    @commands.command(name='sell')
    async def do_sell(self, ctx):
        if unlocked:
            if not ctx.content.count(" ") == 2:
                await ctx.send(f'Usage: !sell <Ticker> <Number of Shares>')
            else:
                ticker = ctx.content.split(" ")[1]
                amount = ctx.content.split(" ")[2]
                try:
                    int(amount)
                    username = ctx.author.name
                    async with aiohttp.ClientSession() as session:
                        r = await fetch(session, "http://localhost:8000/api/stock/" + ticker + "/sell/" + amount + "/user/" + username)
                        if r != '"Trade Successful"':
                            await ctx.send(f'@{ctx.author.name}: ' + r)
                except Exception as e:
                    await ctx.send(f'Usage: !sell <Ticker> <Number of Shares>')

    @commands.command(name='balance')
    async def get_balance(self, ctx):
        await ctx.send(f'https://marketmayhem.io/users/{ctx.author.name}')

    @commands.command(name='lock')
    async def lock_commands(self, ctx):
        global unlocked
        if unlocked:
            unlocked = False
            await ctx.send('Commands Locked Successfully')

    @commands.command(name='unlock')
    async def unlock_commands(self, ctx):
        global unlocked
        if unlocked is False:
            unlocked = True
            await ctx.send('Commands Unlocked Successfully, Welcome To Market Mayhem!')

    @commands.command(name='marketmayhem')
    async def about_market(self, ctx):
        global unlocked
        if unlocked:
            await ctx.send('The market is currently open for trading! Type !buy and !sell for more instructions')
        else:
            await ctx.send('The market is currently closed for trading! Please wait for the next trading period to start!')

    @commands.command(name='status')
    async def get_status(self, ctx):
        global unlocked
        if unlocked:
            await ctx.send('The market is currently open for trading! Type !buy and !sell for more instructions')
        else:
            await ctx.send('The market is currently closed for trading! Please wait for the next trading period to start!')

    @commands.command(name='updatescores')
    async def update_scores(self, ctx):
        try:
            async with aiohttp.ClientSession() as session:
                await fetch(session, "http://localhost:8000/api/update_scores")
                await ctx.send('Scores Successfully Updated')
        except Exception as e:
            print(e.message)
            await ctx.send('An Error Occurred Updating Scores')

    @commands.command(name='mayhemstats')
    async def get_stats(self, ctx):
        try:
            async with aiohttp.ClientSession() as session:
                r = await fetch(session, "http://localhost:8000/api/stats")
                r = ast.literal_eval(r)
                companies = r[0][1]
                tradefees = r[1][1]
                usercount = r[2][1]
                # await ctx.send(r)
                await ctx.send('Unique Companies Owned: %i, Trade Fees Incurred: %i, Unique User Count: %i' % (companies, tradefees, usercount))
        except Exception as e:
            print(e.message)
            await ctx.send('An Error Occurred Updating Scores')


bot = Bot()
bot.run()
