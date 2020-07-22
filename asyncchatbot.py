from twitchio.ext import commands
import time
import aiohttp
import ast
import os

class Bot(commands.Bot):

    def __init__(self, irc_token, api_prefix, channel, nick):
        super().__init__(irc_token=irc_token, nick=nick, prefix='!',
                         initial_channels=[channel])
        self.api_prefix = api_prefix
        self.unlocked = False

    # Events don't need decorators when subclassed
    async def event_ready(self):
        print(f'Ready | {self.nick}')

    async def event_message(self, message):
        await self.handle_commands(message)

    async def fetch(self, session, path):
        async with session.get(self.api_prefix + path) as response:
            return await response.text()

    # Commands use a different decorator
    @commands.command(name='buy')
    async def do_buy(self, ctx):
        if self.unlocked:
            if not ctx.content.count(" ") == 2:
                await ctx.send(f'Usage: !buy <Ticker> <Number of Shares>')
            else:
                ticker = ctx.content.split(" ")[1]
                amount = ctx.content.split(" ")[2]
                try:
                    int(amount)
                    username = ctx.author.name
                    async with aiohttp.ClientSession() as session:
                        r = await self.fetch(session, "/api/stock/" + ticker + "/buy/" + amount + "/user/" + username)
                        # TODO structured data
                        if r != '"Trade Successful"':
                            await ctx.send(f'@{ctx.author.name}: ' + r)
                except Exception as e:
                    print(e.message)
                    await ctx.send(f'Usage: !buy <Ticker> <Number of Shares>')

    @commands.command(name='sell')
    async def do_sell(self, ctx):
        if self.unlocked:
            if not ctx.content.count(" ") == 2:
                await ctx.send(f'Usage: !sell <Ticker> <Number of Shares>')
            else:
                ticker = ctx.content.split(" ")[1]
                amount = ctx.content.split(" ")[2]
                try:
                    int(amount)
                    username = ctx.author.name
                    async with aiohttp.ClientSession() as session:
                        r = await self.fetch(session, "/api/stock/" + ticker + "/sell/" + amount + "/user/" + username)
                        if r != '"Trade Successful"':
                            await ctx.send(f'@{ctx.author.name}: ' + r)
                except Exception as e:
                    print(e.message)
                    await ctx.send(f'Usage: !sell <Ticker> <Number of Shares>')

    @commands.command(name='balance')
    async def get_balance(self, ctx):
        await ctx.send(f'https://marketmayhem.io/users/{ctx.author.name}')

    @commands.command(name='lock')
    async def lock_commands(self, ctx):
        if self.unlocked:
            self.unlocked = False
            await ctx.send('Commands Locked Successfully')

    @commands.command(name='unlock')
    async def unlock_commands(self, ctx):
        if self.unlocked is False:
            self.unlocked = True
            await ctx.send('Commands Unlocked Successfully, Welcome To Market Mayhem!')

    @commands.command(name='marketmayhem')
    async def about_market(self, ctx):
        if self.unlocked:
            await ctx.send('The market is currently open for trading! Type !buy and !sell for more instructions')
        else:
            await ctx.send('The market is currently closed for trading! Please wait for the next trading period to start!')

    @commands.command(name='status')
    async def get_status(self, ctx):
        return self.about_market(ctx)

    @commands.command(name='updatescores')
    async def update_scores(self, ctx):
        try:
            async with aiohttp.ClientSession() as session:
                await self.fetch(session, "/api/update_scores")
                await ctx.send('Scores Successfully Updated')

        except Exception as e:
            print(e.message)
            await ctx.send('An Error Occurred Updating Scores')

    @commands.command(name='mayhemstats')
    async def get_stats(self, ctx):
        try:
            async with aiohttp.ClientSession() as session:
                r = await self.fetch(session, "/api/stats")
                r = ast.literal_eval(r)
                companies = r[0][1]
                tradefees = r[1][1]
                usercount = r[2][1]
                # await ctx.send(r)
                await ctx.send('Unique Companies Owned: %i, Trade Fees Incurred: %i, Unique User Count: %i' % (companies, tradefees, usercount))
        except Exception as e:
            print(e.message)
            await ctx.send('An Error Occurred Updating Scores')

if __name__ == "__main__":
    irc_token = os.getenv('TWITCH_TOKEN', None)
    channel = os.getenv('TWITCH_CHANNEL', None)
    bot_username = os.getenv('BOT_USERNAME', 'MarketMayhem')

    print("channel:%s bot_username:%s" % (channel, bot_username))

    api_prefix = os.getenv('API_PREFIX', 'http://localhost:8000')

    bot = Bot(irc_token, api_prefix, channel, bot_username)
    bot.run()
