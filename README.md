# market-mayhem

## Preparation

1. Have a Twitch Channel.
2. Have a Twitch User to represent the bot.
3. Get a Twitch OAuth token (see [Twitch documentation](https://dev.twitch.tv/docs/irc#overview) and get a quick test token from https://twitchapps.com/tmi). The OAuth token must be for the Twitch User that represents the bot.
4. Have an [IEX Cloud](https://iexcloud.io/) token. Currently the functionality requires a paid account.

## Running

### With Docker (all-in-one container)

1. Install [Docker](https://docs.docker.com/get-docker)
2. Depending on if `sudo` is required, run (in this directory) `docker build --target all-in-one -t market-mayhem:latest && docker run -it --rm -e 'TWITCH_TOKEN=<Twitch OAuth token>' -e 'TWITCH_CHANNEL=<Twitch channel name>' -e 'BOT_USERNAME=<Twitch bot username>' -e 'IEX_TOKEN=<IEX Cloud SK token>' -v '<Existing Redis Data Directory>':'/var/lib/redis' -p 8000:8000 --rm market-mayhem:latest`

### With Docker Compose

1. Install [Docker Compose](https://docs.docker.com/compose/install)
2. If you have prexisting data, either use symbolic links or copy the data into the current directory under `./data` (this feels very clunky, may revisit best approach with `docker-compose`, i.e. use environment variable).
2. Depending on if `sudo` is required, run (in this directory) `docker-compose build && TWITCH_TOKEN='<Twitch OAuth token>' TWITCH_CHANNEL='<Twitch channel name>' BOT_USERNAME='<Twitch bot username>' IEX_TOKEN='<IEX Cloud SK token>' docker-compose up`

### With `venv`

See [`samplestart.sh`](samplestart.sh)

