# market-mayhem

## Running

### With Docker (all-in-one container)

1. Install [Docker](https://docs.docker.com/get-docker)
2. Depending on if `sudo` is required, run (in this directory) `docker build --target all-in-one -t market-mayhem:latest && docker run -it --rm -e TWITCH_TOKEN='<Twitch OAuth token>' -e TWITCH_CHANNEL='<Twitch channel name>' -e BOT_USERNAME='<Twitch bot username>' -e IEX_TOKEN='<IEX Cloud SK token>' --rm market-mayhem:latest`

### With Docker Compose

1. Install [Docker Compose](https://docs.docker.com/compose/install)
2. Depending on if `sudo` is required, run (in this directory) `docker-compose build && TWITCH_TOKEN='<Twitch OAuth token>' TWITCH_CHANNEL='<Twitch channel name>' BOT_USERNAME='<Twitch bot username>' IEX_TOKEN='<IEX Cloud SK token>' docker-compose up`

### With `venv`

See [`samplestart.sh`](samplestart.sh)
