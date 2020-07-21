import sys
import irc.bot
import aiohttp
import asyncio
import time


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()


class TwitchBot(irc.bot.SingleServerIRCBot):
    def __init__(self, username, token, channel):
        self.token = token
        self.channel = '#' + channel

        # Create IRC bot connection
        server = 'irc.chat.twitch.tv'
        port = 6697
        print('Connecting to ' + server + ' on port ' + str(port) + '...')
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port, 'oauth:'+token)], username, username)

    def on_welcome(self, c, e):
        print('Joining ' + self.channel)

        # You must request specific capabilities before you can use them
        c.cap('REQ', ':twitch.tv/membership')
        c.cap('REQ', ':twitch.tv/tags')
        c.cap('REQ', ':twitch.tv/commands')
        c.join(self.channel)
        c.privmsg(self.channel, "Hello!")

    async def on_pubmsg(self, c, e):
        # If a chat message starts with an exclamation point, try to run it as a command
        if e.arguments[0][:1] == '!':
            cmd = e.arguments[0][1:]
            loop = asyncio.get_event_loop()
            loop.run_until_complete(self.do_command(e, cmd))
        return

    async def do_command(self, e, cmd):
            c = self.connection
            # Poll the API to get current game.
            if cmd.startswith('buy'):
                if cmd == "buy":
                    c.privmsg(self.channel, "Usage: !buy <Ticker> <Number of Shares>")
                else:
                    async with aiohttp.ClientSession() as session:
                        ticker = e.arguments[0].split(" ")[1]
                        amount = e.arguments[0].split(" ")[2]
                        username = e.source.split("!")[0]
                        start = time.time()
                        r = await fetch(session,  "http://localhost:8000/api/stock/" + ticker + "/buy/" + amount + "/user/" + username)
                        end = time.time()
                        print(end - start)
                        if r != '"Trade Successful"':
                            c.privmsg(self.channel, ("@" + username + ": " + r))
            if cmd.startswith('sell'):
                if cmd == "sell":
                    c.privmsg(self.channel, "Usage: !sell <Ticker> <Number of Shares>")
                else:
                    async with aiohttp.ClientSession() as session:
                        ticker = e.arguments[0].split(" ")[1]
                        amount = e.arguments[0].split(" ")[2]
                        username = e.source.split("!")[0]
                        start = time.time()
                        r = await fetch(session, "http://localhost:8000/api/stock/" + ticker + "/sell/" + amount + "/user/" + username)
                        end = time.time()
                        print(end - start)
                        if r != '"Trade Successful"':
                            c.privmsg(self.channel, ("@" + username + ": " + r))


def main():
    if len(sys.argv) != 2:
        print("Usage: twitchbot channel")
        sys.exit(1)

    username  = "stuuuk"
    token     = "gye1zcsgefme4wkern5nd3prh7onwy"
    channel   = sys.argv[1]

    bot = TwitchBot(username, token, channel)
    bot.start()


if __name__ == "__main__":
    main()
